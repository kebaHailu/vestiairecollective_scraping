import csv 


class File:
    def read_csv(self,csv_name='data'):
        existing_data = []
        try:
            with open(csv_name+'.csv', 'r', newline='', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    existing_data.append(row)
            return existing_data
        except FileNotFoundError:
            return []
        
    def save_as_csv(self,data,fieldnames,finalname):

        for i in range(len(data)):
            dictdata = data[i]
            temp = dictdata.copy()
            for label in dictdata.keys():
                if label not in fieldnames:
                    del temp[label]
            data[i] = temp.copy()
        with open(finalname, 'w',newline='',encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)