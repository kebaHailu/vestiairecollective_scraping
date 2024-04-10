import csv 

input_file = "data.csv"
output_file = "gbpdata.csv"




#
desired_order = "Image,Name,Discription,Price,price_with_discount,Categories :,Category:,Sub-category:,Designer:,Color:,Link,Size:,Condition:,Location:,Reference:,Material:,Measurement,Model:,Style:,Place of purchase:Online since:".split(',')

with open(input_file, 'r', newline='',encoding='utf-8') as f_input, open(output_file, 'w', newline='',encoding='utf-8') as f_output:
    reader = csv.DictReader(f_input)
    fieldnames = reader.fieldnames

    # Reorder the columns according to the desired order
    reordered_fieldnames = [field for field in desired_order if field in fieldnames]

    writer = csv.DictWriter(f_output, fieldnames=reordered_fieldnames)
    writer.writeheader()

    for row in reader:
        for x in ['Price','price_with_discount']:
            if x in row:
                if row[x]:
                    row[x] = '£' + str(float(row[x][1:].replace(',',''))*0.79)

        reordered_row = {field: row[field] for field in reordered_fieldnames}   
        writer.writerow(reordered_row)