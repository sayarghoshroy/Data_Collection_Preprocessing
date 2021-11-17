# pip install pdfminer.six
import re
import os
import shutil

path_to_folder = "./pdf_converter_module"
path_to_pdfs = "./PDFs"

def get_dir():
    global path_to_pdfs
    while not os.path.isdir(path_to_pdfs):
        print("Enter Path to your Directory with PDF Files")
        path_to_pdfs = input()
    
    return path_to_pdfs

def get_files(path_to_dir):

    all_files = os.listdir(path_to_dir)
    pdf_files = []
    for file in all_files:
        if file.endswith(".pdf"):
            pdf_files.append(file)

    print("Files in Directory: ")
    print(all_files)
    
    print("PDF files in directory: ")
    print(pdf_files)
    return pdf_files

def get_text(file_name):

    global path_to_folder
    debug = True
    if debug == True:
        print('Converting ' + file_name)
    command_string = "python3 " + path_to_folder + "/pdfminer/pdfminer_data/scripts/pdf2txt.py " + file_name + " > temp_out"
    os.system(command_string)

def clean():

    fp = open("temp_out")
    text = fp.read()

    text = re.sub(r"\n[1-9][0-9]*[\n\r\s]", r"", text) # Takes care of page numbers
    text = re.sub(r"\f", r"", text)
    text = re.sub(r" \n", r" ", text)
    text = re.sub(r"ﬀ", r"ff", text)
    text = re.sub(r"ﬃ", r"ffi", text)

    text = re.sub(r"([a-zA-Z\'\,'])\n([a-zA-Z])", r"\1 \2", text)

    text = re.sub(r"  ", r" ", text)
    # Use only if you want to reduce divisions
    # text = re.sub(r" \n", r" ", text)
    text = re.sub(r"\n[\n\r\s]+", r"\n", text)

    text = re.sub(r"([a-zA-Z])\-\n([a-zA-Z])", r"\1-\2",text)

    # Commented out to show intermediates:
    # os.remove("temp_out")
    return text

def make_dir(dir_name):

    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)

def write_file(dir_name, file, result):
    name = dir_name + "/" + file[:-3] + "txt"
    fpt = open(name, "w+")
    fpt.write(result)
    fpt.close()

def process():

    directory = get_dir()
    files = get_files(directory)

    dir_name = directory + "_texts"
    make_dir(dir_name)

    for file in files:
        process_file = directory + "/" + file
        process_file = re.sub(r" ", r"\\ ", process_file) 
        get_text(process_file)
        result = clean()
        write_file(dir_name, file, result)

if __name__ == "__main__":

    check_path = path_to_folder + "/pdfminer/pdfminer_data/scripts/pdf2txt.py"
    while not os.path.isfile(check_path):
        print("Enter path to your Module")
        path_to_folder = input()
        check_path = path_to_folder + "/pdfminer/pdfminer_data/scripts/pdf2txt.py"
    process()