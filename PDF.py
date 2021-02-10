from PIL import Image
import os,math,argparse,random
from time import sleep as nap
# pip3 install PyMuPDF Pillow

class pdf:
    '''This class is can create pdf from the given images ,compress a exiting pdf,create a compressed pdf
    One of the best thing is that you can provide the *size* for the compression
    limitation -> This class is limied to work with images.
    program will update the file if already exist.'''
    def __init__(self,files_lacation,file_name):
        self.image_type = ['PNG','JPG','JPEG','JIFF','TIFF']
        self.pdf_name = ''.join([file_name,'.pdf'])
        self.files_lacation = files_lacation
        self.search_for_image_in_dir(os.listdir(files_lacation))
    
    def open_convert(self,image_path):
        to_print = image_path.rsplit('/',1)[1]
        # print(f"working on '{to_print}' {random.choice(['😀','😁','😎','🤗','😃'])}")
        image = Image.open(image_path)
        return image.convert('RGB')

    def search_for_image_in_dir(self,name_list):
        self.imagelist = []
        for i in name_list:
            image_path = os.path.join(self.files_lacation,i)
            # check if file is not a directory and if exist and is type of image
            if not os.path.isdir(image_path) and os.path.exists(image_path) and image_path.rsplit('.',1)[1].upper() in self.image_type:
#                 print(self.open_convert(image_path))
                self.imagelist.append(self.open_convert(image_path))
    
    @property
    def get_file_size(self):
        # file size in kb in ceil 
        return math.ceil(os.stat(self.pdf_name).st_size /1024)

    def save_compressed_pdf(self,size_needed):
        # set the quality variable at your desired level, The more the value of quality variable and lesser the compression 
        quality = 80 # for about same size
        path_to_save = self.files_lacation.rsplit('/',1)[0]
        self.pdf_name = os.path.join(path_to_save,self.pdf_name)
        def savepdf(quality):
            if len(self.imagelist) > 1:
#                 print(len(self.imagelist))
                self.imagelist[0].save(self.pdf_name,
                                        save_all=True,
                                        append_images=self.imagelist[1:],
                                        optimize = True,
                                        quality = quality)
            else:
#                 print(len(self.imagelist))
                self.imagelist[0].save(self.pdf_name,
                                        save_all=True,
                                        optimize = True,
                                        quality = quality)

        if self.imagelist:
            start,end = 5,quality
            savepdf(70)
            starting_size = self.get_file_size
            while starting_size > size_needed :
                # on every itreation quatiy use half of the range value
                quality = int((start + end) / 2)                
                savepdf(quality)
                current_size = self.get_file_size
                if 10 < (size_needed - current_size) < 60 : 
                    break 
                elif start == end :
                    # print(f"\ncurrent size => {current_size} File can not compress more this is best possible compression from our side.")
                    break
                elif (current_size - size_needed) < 0 :
                    # low then require
                    start = quality
                elif (current_size - size_needed) > 0 :
                    # higher then require
                    end = quality
            
            # try : print(self.pdf_compressed_name + ' PDF compressed size - '+str(current_size)+' kb')
            # except : print(self.pdf_compressed_name + ' PDF is already smaller then needed compressed size is  - '+str(starting_size)+' kb')

        return self.get_file_size

    @classmethod
    def create_compressed_pdf(cls,directory,file_name,size_needed = 1024):
        pdf = cls(directory,file_name)
        return pdf.save_compressed_pdf(size_needed)

if __name__ == "__main__" :
    pass
    # example print(pdf.create_compressed_pdf(path_to_folder,file_name))
