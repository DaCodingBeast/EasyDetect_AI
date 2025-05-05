import csv

class Dataset():
    def __init__(self,framesPerSample, filename= "pose_data.csv"):
        self.framesPerSample = framesPerSample
        self.filename = filename
        self.count = 0

        with open(filename,'w') as file:
            writer = csv.writer(file)
            heading = ["count", "label"]

            for i in range(72):
                
                detirmineType = {
                    0: "x",
                    1: "y",
                    2: "z"
                }
                heading.append(f"{i//3}{detirmineType[i%3]}")

            writer.writerow(heading)

        
    def addToDataset(self,points:list ,label:str = None):
        with open(self.filename, 'a',newline='') as file:
            writer = csv.writer(file)
            rows = points

            for row in rows:
                row.insert(0,self.count)
                if label:
                    row.insert(1,label)
                writer.writerow(row)

        self.count +=1

    def getDataset(file_name,framesPerSample):
        pointDataset = []
        labelDataset = []
        with open(file_name,'r') as file:
            data = csv.reader(file)
            next(data)
            next(data)

            sampleOfData =[]
            for index, row in enumerate(data):
                row.pop(0)
                label = row.pop(0)

                sampleOfData.append(row)
                # print(index)
                # print(row)

                if((index+1) % framesPerSample ==0 and index !=0):
                    labelDataset.append(label)
                    pointDataset.append(sampleOfData)
                    # print(sampleOfData)
                    sampleOfData = []

        return pointDataset,labelDataset
    

    def getFlattenedDataset(file_name,framesPerSample):
        pointDataset = []
        labelDataset = []
        with open(file_name,'r') as file:
            data = csv.reader(file)
            next(data)
            next(data)

            sampleOfData =[]
            for index, row in enumerate(data):
                row.pop(0)
                label = row.pop(0)

                sampleOfData.append(row)

                if((index+1) % framesPerSample ==0 and index !=0):
                    labelDataset.append(label)

                    combined_list = [item for sublist in sampleOfData for item in sublist]

                    pointDataset.append(combined_list)
                    sampleOfData = []

        return pointDataset,labelDataset
    
    def getFlattened_TestData(data, framesPerSample):
        pointDataset = []
        sampleOfData =[]
        for index, row in enumerate(data):
            sampleOfData.append(row)

            if((index+1) % framesPerSample ==0 and index !=0):
                    combined_list = [item for sublist in sampleOfData for item in sublist]

                    pointDataset.append(combined_list)
                    sampleOfData = []

        return pointDataset
    
    def clear(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

        with open(self.filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
