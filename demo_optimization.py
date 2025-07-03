#!/usr/bin/env python3
"""
Demonstration script showing the difference between:
1. Old approach: Complete overwriting with Gemini response
2. New approach: Intelligent optimization preserving original content
"""

from gemini_project_analyzer import SmartGeminiAnalyzer, OptimizationLevel
import os

def demo_old_vs_new_approach():
    """Demonstrate the difference between overwriting and optimizing"""
    
    # Sample content to optimize
    sample_content = """
# Project Overview
This is our new mobile app idea.

## Key Features
- User authentication system
- Real-time messaging capabilities 
- File sharing functionality
- Push notifications support

## Technical Requirements
The app should be built using React Native for cross-platform compatibility. 
We need to integrate with Firebase for backend services.
The user interface must be intuitive and follow material design principles.

## Timeline
Development should take approximately 3 months.
Testing phase will require additional 2 weeks.
Deployment to app stores expected by end of Q4.
"""

    print("🔍 DEMONSTRATION: Old vs New Optimization Approach")
    print("=" * 60)
    
    print("\n📄 ORIGINAL CONTENT:")
    print("-" * 30)
    print(sample_content)
    
    # Simulate old approach (complete overwriting)
    print("\n❌ OLD APPROACH - Complete Overwriting:")
    print("-" * 40)
    old_approach_result = """
# Enhanced Mobile Application Concept

## Revolutionary Features
- Advanced authentication with biometric integration
- Real-time communication platform with video capabilities
- Comprehensive file management with cloud synchronization
- Intelligent push notification system with ML-powered personalization

## Technical Architecture
Utilize React Native framework for optimal cross-platform development.
Implement Firebase ecosystem for robust backend infrastructure.
Design responsive UI following Google's Material Design 3 guidelines.

## Project Timeline
Initial development cycle: 12-16 weeks
Quality assurance testing: 3-4 weeks  
App store submission and approval: Q4 target
"""
    print(old_approach_result)
    print(f"❗ PRESERVATION RATIO: ~30% (Most content completely rewritten)")
    
    # Try new approach if API key is available
    try:
        analyzer = SmartGeminiAnalyzer()
        
        print("\n✅ NEW APPROACH - Intelligent Optimization:")
        print("-" * 45)
        
        # Light optimization
        print("\n🔹 LIGHT OPTIMIZATION (90%+ preservation):")
        light_result = analyzer.optimize_content_intelligently(
            sample_content, 
            OptimizationLevel.LIGHT
        )
        print(light_result.optimized_content)
        print(f"📊 Preservation ratio: {light_result.preservation_ratio:.1%}")
        print(f"📝 {light_result.changes_summary}")
        
        # Moderate optimization  
        print("\n🔸 MODERATE OPTIMIZATION (70%+ preservation):")
        moderate_result = analyzer.optimize_content_intelligently(
            sample_content,
            OptimizationLevel.MODERATE
        )
        print(moderate_result.optimized_content)
        print(f"📊 Preservation ratio: {moderate_result.preservation_ratio:.1%}")
        print(f"📝 {moderate_result.changes_summary}")
        
    except Exception as e:
        print(f"\n⚠️  Could not demonstrate new approach: {e}")
        print("💡 To see live optimization, set GEMINI_API_KEY environment variable")
        
        # Show simulated new approach results
        print("\n✅ NEW APPROACH - Simulated Results:")
        print("-" * 40)
        
        simulated_light = """
# Project Overview
This is our new mobile application idea.

## Key Features
- User authentication system
- Real-time messaging capabilities
- File sharing functionality  
- Push notifications support

## Technical Requirements
The app should be built using React Native for cross-platform compatibility.
We need to integrate with Firebase for backend services.
The user interface must be intuitive and follow Material Design principles.

## Timeline
Development should take approximately 3 months.
Testing phase will require an additional 2 weeks.
Deployment to app stores expected by end of Q4.
"""
        
        print("🔹 LIGHT OPTIMIZATION (simulated):")
        print(simulated_light)
        print("📊 Preservation ratio: ~95% (Minor grammar and clarity improvements)")
        
        simulated_moderate = """
# Project Overview
This is our innovative new mobile application concept.

## Core Features
- Secure user authentication system
- Real-time messaging with enhanced capabilities
- Seamless file sharing functionality
- Intelligent push notifications support

## Technical Requirements
The application will be developed using React Native to ensure optimal cross-platform compatibility.
We will integrate with Firebase to provide robust backend services.
The user interface must be intuitive and adhere to modern Material Design principles.

## Development Timeline
• Development phase: approximately 3 months
• Testing and quality assurance: additional 2 weeks  
• App store deployment: targeted for end of Q4
"""
        
        print("\n🔸 MODERATE OPTIMIZATION (simulated):")
        print(simulated_moderate)
        print("📊 Preservation ratio: ~80% (Enhanced clarity while preserving structure)")

def demo_section_analysis():
    """Demonstrate how content is analyzed in sections"""
    
    print("\n\n🔍 SECTION ANALYSIS DEMONSTRATION")
    print("=" * 40)
    
    sample_text = """
# Important Header
This is a critical paragraph with key information.

## Secondary Header  
This paragraph has moderate importance.

• Bullet point one
• Bullet point two
• Bullet point three

Regular paragraph at the end.
"""
    
    print("📄 Sample content:")
    print(sample_text)
    
    print("\n📊 How the new system analyzes content:")
    print("Section 1: '# Important Header' -> Type: header, Importance: 0.9, Target: minimal_changes")
    print("Section 2: 'This is a critical...' -> Type: paragraph, Importance: 0.8, Target: clarity_and_flow") 
    print("Section 3: '## Secondary Header' -> Type: header, Importance: 0.9, Target: minimal_changes")
    print("Section 4: 'This paragraph has...' -> Type: paragraph, Importance: 0.8, Target: clarity_and_flow")
    print("Section 5: '• Bullet point...' -> Type: bullet_point, Importance: 0.7, Target: clarity_and_flow")
    print("Section 6: 'Regular paragraph...' -> Type: paragraph, Importance: 0.8, Target: clarity_and_flow")
    
    print("\n💡 Each section is optimized independently based on its:")
    print("   • Type and structure")
    print("   • Importance score") 
    print("   • Optimization target")
    print("   • Chosen optimization level")

if __name__ == "__main__":
    demo_old_vs_new_approach()
    demo_section_analysis()
    
    print("\n\n🎯 KEY IMPROVEMENTS:")
    print("=" * 30)
    print("✅ Preserves original structure and meaning")
    print("✅ Offers multiple optimization levels") 
    print("✅ Analyzes content in sections for targeted improvement")
    print("✅ Provides preservation ratio metrics")
    print("✅ Maintains author's voice and intent")
    print("✅ Fallback handling when optimization fails")
    print("✅ Detailed logging and error handling")
    
    print("\n📖 USAGE EXAMPLES:")
    print("=" * 20)
    print("# Light optimization (preserve 90%+)")
    print("python gemini_project_analyzer.py document.txt -l light -o optimized.txt")
    print("\n# Moderate optimization (preserve 70%+)")  
    print("python gemini_project_analyzer.py document.docx -l moderate -o improved.txt")
    print("\n# Comprehensive optimization")
    print("python gemini_project_analyzer.py document.pdf -l comprehensive -o enhanced.txt")