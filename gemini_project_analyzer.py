#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Optimized Gemini Project Analyzer v4

• Intelligently enhances documents while preserving original structure
• Selective optimization instead of complete overwriting
• Multiple optimization levels: light, moderate, comprehensive
• Maintains original intent while improving clarity and quality
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, GoogleAPICallError
from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError
import docx
import openpyxl
import PyPDF2

# Load environment variables
load_dotenv()

class OptimizationLevel(Enum):
    LIGHT = "light"           # Minor improvements, preserve 90%+ of original
    MODERATE = "moderate"     # Balanced enhancement, preserve 70%+ of original  
    COMPREHENSIVE = "comprehensive"  # Major improvements, preserve core structure

@dataclass
class ContentSection:
    """Represents a section of content with metadata for targeted optimization"""
    original_text: str
    section_type: str  # header, paragraph, bullet_point, etc.
    importance_score: float  # 0-1, how critical this section is
    optimization_target: str  # clarity, structure, completeness, etc.

@dataclass
class OptimizationResult:
    """Result of content optimization with preserved original"""
    original_content: str
    optimized_content: str
    changes_summary: str
    preservation_ratio: float  # How much of original was preserved

class SmartGeminiAnalyzer:
    """Intelligent document analyzer that enhances rather than overwrites content"""
    
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-pro-latest"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable must be set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.prompts = self._load_prompts()
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the analyzer"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gemini_analyzer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load prompts from JSON file"""
        try:
            with open("gemini_project_analyzer.prompts.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Prompts file not found, using default prompts")
            return self._get_default_prompts()
    
    def _get_default_prompts(self) -> Dict[str, str]:
        """Default prompts for optimization tasks"""
        return {
            "enhance_content": """
            Enhance the following content while preserving its original structure and key information.
            Optimization level: {level}
            
            Guidelines:
            - PRESERVE the original meaning and intent
            - Improve clarity and readability without changing core message
            - Maintain original structure (headers, bullets, formatting)
            - For LIGHT: Minor improvements only (grammar, word choice)
            - For MODERATE: Balanced enhancement (clarity, flow, some restructuring)
            - For COMPREHENSIVE: Significant improvements while keeping core intact
            
            Original content:
            {content}
            
            Return the enhanced version with explanations of changes made.
            """,
            
            "analyze_sections": """
            Analyze this content and identify distinct sections that could be optimized.
            For each section, determine:
            1. Section type (header, paragraph, list, etc.)
            2. Importance score (0-1)
            3. What type of optimization would benefit it most
            
            Content:
            {content}
            
            Return as structured data showing analysis results.
            """,
            
            "preserve_and_enhance": """
            Take this content and enhance ONLY the specified aspects while preserving everything else:
            
            Target for enhancement: {target}
            Preservation priority: {preservation_level}
            
            Original content:
            {content}
            
            Rules:
            - Keep original structure intact
            - Only modify what directly relates to the enhancement target
            - Preserve all key information and facts
            - Maintain the author's voice and style
            """
        }
    
    def _call_gemini_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Call Gemini API with retry logic and rate limiting"""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    return response.text
                else:
                    self.logger.warning(f"Empty response from Gemini on attempt {attempt + 1}")
            except ResourceExhausted:
                wait_time = 2 ** attempt
                self.logger.warning(f"Rate limit hit, waiting {wait_time} seconds...")
                time.sleep(wait_time)
            except (ServiceUnavailable, GoogleAPICallError) as e:
                self.logger.error(f"API error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)
        
        raise Exception("Failed to get response from Gemini after all retries")
    
    def analyze_content_structure(self, content: str) -> List[ContentSection]:
        """Analyze content to identify sections for targeted optimization"""
        prompt = self.prompts.get("analyze_sections", "").format(content=content)
        
        try:
            analysis = self._call_gemini_with_retry(prompt)
            # Parse the analysis to extract sections
            sections = self._parse_section_analysis(content, analysis)
            return sections
        except Exception as e:
            self.logger.error(f"Error analyzing content structure: {e}")
            # Fallback: treat entire content as single section
            return [ContentSection(
                original_text=content,
                section_type="full_document",
                importance_score=1.0,
                optimization_target="general_improvement"
            )]
    
    def _parse_section_analysis(self, original_content: str, analysis: str) -> List[ContentSection]:
        """Parse Gemini's analysis to create ContentSection objects"""
        sections = []
        
        # Simple heuristic-based parsing - split by paragraphs for now
        # In a production system, this would be more sophisticated
        paragraphs = [p.strip() for p in original_content.split('\n\n') if p.strip()]
        
        for i, paragraph in enumerate(paragraphs):
            # Determine section type
            if paragraph.startswith('#') or paragraph.isupper():
                section_type = "header"
                importance = 0.9
            elif paragraph.startswith('•') or paragraph.startswith('-') or paragraph.startswith('*'):
                section_type = "bullet_point"
                importance = 0.7
            else:
                section_type = "paragraph"
                importance = 0.8
            
            sections.append(ContentSection(
                original_text=paragraph,
                section_type=section_type,
                importance_score=importance,
                optimization_target="clarity_and_flow"
            ))
        
        return sections
    
    def optimize_content_intelligently(
        self, 
        content: str, 
        optimization_level: OptimizationLevel = OptimizationLevel.MODERATE,
        preserve_structure: bool = True
    ) -> OptimizationResult:
        """Intelligently optimize content while preserving original structure"""
        
        self.logger.info(f"Starting intelligent optimization with level: {optimization_level.value}")
        
        # Step 1: Analyze content structure
        sections = self.analyze_content_structure(content)
        
        # Step 2: Optimize each section based on its characteristics
        optimized_sections = []
        total_preservation_score = 0.0
        
        for section in sections:
            optimized_section = self._optimize_section(section, optimization_level, preserve_structure)
            optimized_sections.append(optimized_section)
            
            # Calculate preservation ratio for this section
            preservation = self._calculate_preservation_ratio(section.original_text, optimized_section)
            total_preservation_score += preservation * section.importance_score
        
        # Step 3: Combine optimized sections while maintaining structure
        if preserve_structure:
            optimized_content = self._reconstruct_with_structure(content, sections, optimized_sections)
        else:
            optimized_content = '\n\n'.join(optimized_sections)
        
        # Step 4: Create summary of changes
        changes_summary = self._generate_changes_summary(content, optimized_content, sections)
        
        # Calculate overall preservation ratio
        overall_preservation = total_preservation_score / len(sections) if sections else 1.0
        
        return OptimizationResult(
            original_content=content,
            optimized_content=optimized_content,
            changes_summary=changes_summary,
            preservation_ratio=overall_preservation
        )
    
    def _optimize_section(
        self, 
        section: ContentSection, 
        optimization_level: OptimizationLevel,
        preserve_structure: bool
    ) -> str:
        """Optimize a single content section"""
        
        # Adjust optimization intensity based on importance and level
        if section.importance_score > 0.8 and optimization_level == OptimizationLevel.LIGHT:
            # High importance + light optimization = minimal changes
            target = "grammar_and_style_only"
            preservation = "maximum"
        elif optimization_level == OptimizationLevel.COMPREHENSIVE:
            target = section.optimization_target
            preservation = "moderate"
        else:
            target = "clarity_and_readability"
            preservation = "high"
        
        prompt = self.prompts.get("preserve_and_enhance", "").format(
            target=target,
            preservation_level=preservation,
            content=section.original_text
        )
        
        try:
            optimized = self._call_gemini_with_retry(prompt)
            # Extract just the optimized content, remove any explanations
            return self._extract_optimized_content(optimized, section.original_text)
        except Exception as e:
            self.logger.error(f"Error optimizing section: {e}")
            return section.original_text  # Return original if optimization fails
    
    def _extract_optimized_content(self, gemini_response: str, original: str) -> str:
        """Extract the actual optimized content from Gemini's response"""
        # Try to find content between common markers
        patterns = [
            r"Enhanced version:\s*(.*?)(?:\n\nExplanation|$)",
            r"Optimized content:\s*(.*?)(?:\n\nChanges|$)",
            r"Result:\s*(.*?)(?:\n\nSummary|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, gemini_response, re.DOTALL | re.IGNORECASE)
            if match:
                extracted = match.group(1).strip()
                if extracted and len(extracted) > len(original) * 0.3:  # Sanity check
                    return extracted
        
        # If no clear extraction, return the response but clean it up
        lines = gemini_response.split('\n')
        content_lines = []
        skip_explanatory = False
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['explanation', 'changes made', 'summary', 'analysis']):
                skip_explanatory = True
                continue
            if not skip_explanatory and line and not line.startswith('•') and not line.startswith('-'):
                content_lines.append(line)
        
        result = '\n'.join(content_lines).strip()
        return result if result else original
    
    def _reconstruct_with_structure(
        self, 
        original: str, 
        sections: List[ContentSection], 
        optimized_sections: List[str]
    ) -> str:
        """Reconstruct the content while preserving original structure"""
        # Simple reconstruction - maintain paragraph breaks and structure
        result = original
        
        for section, optimized in zip(sections, optimized_sections):
            # Replace the original section with optimized version
            result = result.replace(section.original_text, optimized, 1)
        
        return result
    
    def _calculate_preservation_ratio(self, original: str, optimized: str) -> float:
        """Calculate how much of the original content was preserved"""
        original_words = set(original.lower().split())
        optimized_words = set(optimized.lower().split())
        
        if not original_words:
            return 1.0
        
        preserved_words = original_words.intersection(optimized_words)
        return len(preserved_words) / len(original_words)
    
    def _generate_changes_summary(
        self, 
        original: str, 
        optimized: str, 
        sections: List[ContentSection]
    ) -> str:
        """Generate a summary of what changes were made"""
        preservation_ratio = self._calculate_preservation_ratio(original, optimized)
        
        summary = f"Optimization completed with {preservation_ratio:.1%} content preservation.\n"
        summary += f"Processed {len(sections)} content sections.\n"
        
        if preservation_ratio > 0.8:
            summary += "Changes: Minor improvements to clarity and readability."
        elif preservation_ratio > 0.6:
            summary += "Changes: Moderate enhancements while preserving core content."
        else:
            summary += "Changes: Significant improvements with structural preservation."
        
        return summary
    
    def process_document(
        self, 
        file_path: str, 
        optimization_level: OptimizationLevel = OptimizationLevel.MODERATE,
        output_path: str = None
    ) -> OptimizationResult:
        """Process a document file and optimize its content"""
        
        self.logger.info(f"Processing document: {file_path}")
        
        # Extract content based on file type
        content = self._extract_content_from_file(file_path)
        
        if not content:
            raise ValueError(f"Could not extract content from {file_path}")
        
        # Optimize the content
        result = self.optimize_content_intelligently(content, optimization_level)
        
        # Save optimized version if output path provided
        if output_path:
            self._save_optimized_content(result.optimized_content, output_path)
            self.logger.info(f"Optimized content saved to: {output_path}")
        
        return result
    
    def _extract_content_from_file(self, file_path: str) -> str:
        """Extract text content from various file types"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            if path.suffix.lower() == '.txt':
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif path.suffix.lower() == '.docx':
                doc = docx.Document(path)
                return '\n\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
            
            elif path.suffix.lower() == '.pdf':
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    return '\n\n'.join([page.extract_text() for page in reader.pages])
            
            else:
                raise ValueError(f"Unsupported file type: {path.suffix}")
                
        except Exception as e:
            self.logger.error(f"Error extracting content from {file_path}: {e}")
            raise
    
    def _save_optimized_content(self, content: str, output_path: str):
        """Save optimized content to file"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    """Command-line interface for the Smart Gemini Analyzer"""
    parser = argparse.ArgumentParser(description="Smart Gemini Project Analyzer - Enhance content intelligently")
    parser.add_argument("input_file", help="Input file to process")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-l", "--level", choices=["light", "moderate", "comprehensive"], 
                       default="moderate", help="Optimization level")
    parser.add_argument("--preserve-structure", action="store_true", default=True,
                       help="Preserve original document structure")
    parser.add_argument("--model", default="gemini-1.5-pro-latest", help="Gemini model to use")
    
    args = parser.parse_args()
    
    try:
        analyzer = SmartGeminiAnalyzer(model_name=args.model)
        optimization_level = OptimizationLevel(args.level)
        
        result = analyzer.process_document(
            args.input_file, 
            optimization_level=optimization_level,
            output_path=args.output
        )
        
        print(f"\n✅ Optimization completed!")
        print(f"📊 Preservation ratio: {result.preservation_ratio:.1%}")
        print(f"📝 Changes summary: {result.changes_summary}")
        
        if args.output:
            print(f"💾 Optimized content saved to: {args.output}")
        else:
            print("\n🔍 Optimized content:")
            print("=" * 50)
            print(result.optimized_content)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
