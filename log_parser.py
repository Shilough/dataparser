import tkinter as tk
from tkinter import filedialog
import os

root=tk.Tk()
root.withdraw()

input_file_path = filedialog.askopenfilename(
    title="Select Log File",
    filetypes=[("Log Files","*.log"), ("Text Files","*.txt"), ("All Files","*.*")]
)

if not input_file_path:
    print("No file selected. Exiting program.")
    exit()

#Text file data exctraction using Boolean Switch method

capture = False
count = 0
with open(input_file_path,"r") as f:
    num_atom=[] #This will store the atom numbers 
    atom=[] #This will store the elements or atom types
    charge=[] # This will store the atomic charges
    n=44 #This is the number of atoms in the molecule
    for line in f:
        if "Charges from ESP fit," in line:
            capture = True
            num_atom.clear()
            atom.clear()
            charge.clear()
            count = -3
        if capture and count >= 0:
            #print(line, end="")
            #Splits a line from the text file into 3 segments of bits containing the atom number, the atom type, and the charge of the atom in e
            parts = line.split()
            #Assigns a temporary variable to the values in the line
            atom_num = parts[0]
            atom_name = parts[1]
            charge_value = float(parts[2])
            #Appends the values to the lists defined above
            atom.append(atom_name)
            charge.append(charge_value)
            num_atom.append(atom_num)
            count+=1
        elif capture and count <= 0:
            count+=1
            continue
        if count==n:
            capture = False
            count=0
#print(num_atom)
#print(atom)
#print(charge)

#Recombining the data into a CSV
output_folder = os.path.dirname(input_file_path)
output_csv_path = os.path.join(output_folder, "charge.csv" )
n=0
with open(output_csv_path,"w") as f:
    for i in charge:
        f.write(num_atom[n])
        f.write(",")
        f.write(atom[n])
        f.write(",")
        f.write(str(charge[n]))
        f.write("\n")
        n+=1
with open(output_csv_path) as f:
    print(f.read())