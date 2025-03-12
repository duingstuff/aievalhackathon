import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Response Evaluator",
    page_icon="🤖",
    layout="wide"
)

# Custom color scheme
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #2c3e50;
    }
    .answer-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #000000;
        cursor: pointer;
    }
    .selected {
        background-color: #e8f5e9;
        border: 2px solid #4caf50;
    }
    .unselected {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
    }
    .next-button>button {
        background-color: #4caf50;
        color: white;
    }
    .previous-button>button {
        background-color: #90a4ae;
        color: white;
    }
    .save-button>button {
        background-color: #2196f3;
        color: white;
    }
    .question-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .sidebar .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .progress-bar {
        height: 10px;
        background-color: #bbdefb;
    }
    .stProgress > div > div > div {
        background-color: #1976d2;
    }
    .question-text {
        color: #000000;
        font-size: 16px;
    }
    .option-text {
        color: #000000;
    }
    /* Make text area white background */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
    }
    /* Make text area label black */
    .stTextArea label {
        color: #000000 !important;
    }
    /* Make option labels black */
    .option-label {
        color: #000000;
        font-weight: bold;
    }
    /* Hide the radio buttons */
    div[data-testid="stRadio"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Function to load data from JSONL file
def load_data(file_path):
    data = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"Invalid JSON format in file: {file_path}")
        return []

# Function to save evaluation results
def save_evaluation(results, output_file):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    
    # Also save as JSONL for compatibility
    with open(output_file.replace('.csv', '.jsonl'), 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

# Main app
def main():
    # Sidebar styling
    st.sidebar.markdown("""
    <div style="background-color: #1976d2; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar content
    with st.sidebar:
        data_file = st.text_input("Evaluation dataset path", "eval_dataset.jsonl")
        output_path = st.text_input("Output directory", "evaluation_results")
        evaluator_name = st.text_input("Evaluator Name", "Evaluator")
        include_alternative = st.checkbox("Include alternative responses", True)
        
        if st.button("Load Data", key="load_data"):
            st.session_state.data = load_data(data_file)
            st.session_state.current_index = 0
            st.session_state.results = []
            st.session_state.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.output_file = f"{output_path}/{evaluator_name}_{st.session_state.timestamp}.csv"
            
            # Initialize a list to track option order for each question
            st.session_state.option_orders = {}
    
    # Initialize session state for selected option
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
        
    # Initialize option orders if not present
    if 'option_orders' not in st.session_state:
        st.session_state.option_orders = {}
    
    # Main content
    st.markdown("""
    <h1 style="color: #1976d2; text-align: center; margin-bottom: 30px;">Human-in-the-Loop: AI Response Evaluator</h1>
    """, unsafe_allow_html=True)
    
    if 'data' not in st.session_state:
        st.info("👈 Please configure the evaluation settings and load data from the sidebar.")
        return
    
    if not st.session_state.data:
        st.warning("No data loaded or empty dataset.")
        return
    
    # Display progress
    total_items = len(st.session_state.data)
    current = st.session_state.current_index + 1
    st.progress(current / total_items)
    st.markdown(f"<p style='text-align: center; color: #546e7a;'>Question {current} of {total_items}</p>", unsafe_allow_html=True)
    
    # Get current question
    current_item = st.session_state.data[st.session_state.current_index]
    question_id = f"question_{st.session_state.current_index}"
    
    # Display question
    st.markdown(f'<p class="big-font">Question:</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-box question-text">{current_item["input"]}</div>', unsafe_allow_html=True)
    
    # Create options
    options = [
        {"label": "A", "response": current_item["output"]},
    ]
    
    # Add alternative option if enabled
    if include_alternative:
        # For demo, we'll use the next item's output as an alternative
        # In a real scenario, you'd want to use actual alternative responses
        alt_index = (st.session_state.current_index + 1) % len(st.session_state.data)
        alt_response = st.session_state.data[alt_index]["output"]
        options.append({"label": "B", "response": alt_response})
    
    # Display options
    st.markdown(f'<p class="big-font">Select the best answer:</p>', unsafe_allow_html=True)
    
    # Create columns for options
    cols = st.columns(len(options))
    
    # Display options with clickable boxes
    for i, option in enumerate(options):
        with cols[i]:
            # Create a unique key for each button
            key = f"option_{option['label']}_{st.session_state.current_index}"
            
            # Check if this option is selected
            is_selected = st.session_state.selected_option == option["label"]
            selected_class = "selected" if is_selected else "unselected"
            
            # Create a clickable container with the option text
            if st.button(
                f"Option {option['label']}",
                key=key,
                help=f"Click to select Option {option['label']}",
                use_container_width=True
            ):
                st.session_state.selected_option = option["label"]
                st.rerun()
            
            # Display the option content
            st.markdown(
                f'<div class="answer-box {selected_class}"><span class="option-label">Option {option["label"]}:</span><br><span class="option-text">{option["response"]}</span></div>',
                unsafe_allow_html=True
            )
    
    # Comments with white background
    comments = st.text_area("Additional comments (optional)")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="previous-button">', unsafe_allow_html=True)
        if st.button("Previous", disabled=st.session_state.current_index == 0):
            # Reset selection for new question
            st.session_state.selected_option = None
            st.session_state.current_index -= 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="save-button">', unsafe_allow_html=True)
        if st.button("Save & Finish"):
            # Check if an option is selected
            if st.session_state.selected_option is None:
                st.error("Please select an option before saving")
                return
                
            # Save current evaluation
            selected_option = next((option for option in options if option["label"] == st.session_state.selected_option), None)
            is_correct = selected_option["response"] == current_item["output"] if selected_option else False
            
            result = {
                "question_index": st.session_state.current_index,
                "question": current_item["input"],
                "ground_truth": current_item["output"],
                "selected_option": st.session_state.selected_option,
                "selected_response": selected_option["response"] if selected_option else "",
                "is_correct": is_correct,
                "comments": comments,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.results.append(result)
            
            # Save all results
            save_evaluation(st.session_state.results, st.session_state.output_file)
            
            # Display success message with nicer styling
            st.markdown(f"""
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 5px solid #4caf50;">
                <h3 style="color: #2e7d32; margin-top: 0;">Evaluation Saved!</h3>
                <p style="color: #000000;">Results saved to: {st.session_state.output_file}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display summary
            correct_count = sum(1 for r in st.session_state.results if r["is_correct"])
            total_evaluated = len(st.session_state.results)
            
            st.markdown(f"""
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 15px;">
                <h3 style="color: #000000; margin-top: 0;">Evaluation Summary</h3>
                <p style="color: #000000;">Total questions evaluated: {total_evaluated}</p>
                <p style="color: #000000;">Correct selections: {correct_count} ({correct_count/total_evaluated*100:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="next-button">', unsafe_allow_html=True)
        if st.button("Next", disabled=st.session_state.current_index == len(st.session_state.data) - 1):
            # Check if an option is selected
            if st.session_state.selected_option is None:
                st.error("Please select an option before proceeding")
                return
                
            # Save current evaluation
            selected_option = next((option for option in options if option["label"] == st.session_state.selected_option), None)
            is_correct = selected_option["response"] == current_item["output"] if selected_option else False
            
            result = {
                "question_index": st.session_state.current_index,
                "question": current_item["input"],
                "ground_truth": current_item["output"],
                "selected_option": st.session_state.selected_option,
                "selected_response": selected_option["response"] if selected_option else "",
                "is_correct": is_correct,
                "comments": comments,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.results.append(result)
            
            # Reset selection for next question
            st.session_state.selected_option = None
            st.session_state.current_index += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()