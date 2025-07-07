"""
Simplified version of BrandTone to troubleshoot connection issues.
"""
import streamlit as st

def main():
    """Simplified Streamlit application."""
    
    st.title("BrandTone - Simple Test Version")
    st.write("This is a simplified version for testing connectivity.")
    
    # Simple input and output
    input_text = st.text_area("Enter some text:", value="Sample marketing text to transform.")
    tone = st.selectbox("Select tone:", ["casual", "formal", "playful", "technical"])
    
    if st.button("Process"):
        st.write(f"You selected the '{tone}' tone.")
        st.write("Transformed text would appear here.")
        st.success("If you can see this, the application is working correctly!")

if __name__ == "__main__":
    main()
