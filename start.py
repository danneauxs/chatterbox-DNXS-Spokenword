from main_launcher import main, main_with_resume
from wrapper.chunk_tool import run_chunk_repair_tool



def prompt_menu(options):
    print("\nSelect an option:")
    for idx, label in enumerate(options, 1):
        print(f" [{idx}] {label}")
    print(" [0] Exit")

    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                print("Exiting. See you next time!")
                return None
            if 1 <= idx <= len(options):
                return idx
        print("Invalid input. Please enter a valid number.")

def wrapper_main():
    options = [
        "Convert a book (GenTTS)",
        "Resume processing",
        "Combine audio chunks only",
        "Test chunking logic",
        "Launch Chunk Repair / Revision Tool"
    ]

    while True:
        selected = prompt_menu(options)
        if selected is None:
            break
        elif selected == 1:
            main()
        elif selected == 2:
            main_with_resume()
        elif selected == 3:
            run_combine_only_mode()
        elif selected == 4:
            from modules.text_processor import test_chunking
            test_chunking()
        elif selected == 5:
            run_chunk_repair_tool()

if __name__ == "__main__":
    wrapper_main()
