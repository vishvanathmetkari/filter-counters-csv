import pandas as pd
import csv
import os

def delete_rows(filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    data = data[2:]
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def get_formated_data(filename,headers):
    data1=pd.read_csv(filename)
    data1.columns = headers
    pivot_data1 = pd.pivot_table(data1,index=['time','core'], columns=['event'], values=['count'], aggfunc="sum",fill_value=0)
    pivot_data1.reset_index().to_csv('output.csv', index=False)

def add_ipc_value_col(input_file,output_file):

    data = []
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        header = next(reader)
        header = header[0].split(",")
        second_row = next(reader)
        second_row = second_row[0].split(",")
        cycles_col = None
        instructions_col = None
        for i in range(len(header)):
            if second_row[i] == '':
                second_row[i] = header[i]
        # Identify the columns for "cycles" and "instructions"
        for i, col_name in enumerate(second_row):
            if col_name == "cycles":
                cycles_col = i
            elif col_name == "instructions":
                instructions_col = i

        # Check if both "cycles" and "instructions" columns were found
        if cycles_col is not None and instructions_col is not None:
            second_row.append("ipc")  # Add the new column header
            for row in reader:
                try:
                    row =row[0].split(",")
                    cycles = int(row[cycles_col])
                    instructions = int(row[instructions_col])
                    try:
                        row.append(round(instructions / cycles, 2))
                    except:
                        row.append(float(0.00))
                    data.append(row)
                except Exception as e:
                    print("Error: ",e)
        else:
            print("Columns for 'cycles' and 'instructions' not found in the second row.")

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(list(second_row))
        writer.writerows(data)
    if os.path.exists(input_file):
        os.remove(input_file)
    else:
        print(f"{input_file} does not exist.")

if __name__ == '__main__':
    import os
    folder_path = './set7'
    files_in_set7 = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for file in files_in_set7:
        filename = file.replace('\\',"/")
        print("processing ...",filename)
        output_file = "counters-{}".format(filename.split("/")[-1])
        header_names = ['time', 'core','nan-1','count','nan-2', 'event','ipc','nan-3','nan-4', 'nan-5']  # Replace with your desired header names
        delete_rows(filename)
        get_formated_data(filename,header_names)
        add_ipc_value_col('output.csv',output_file)
        print("Data has been transformed and saved to", output_file)
