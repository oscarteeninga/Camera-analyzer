import glob
import os


class Customizer:
    def __init__(self, training_folder, file_name):
        self.file = open(file_name, "w")
        self.training_folder = training_folder
        self.images_list = glob.glob(training_folder + "/*.jpg")
        os.system(
            "echo 'classes = 1\ntrain = custom/train.txt\nvalid = test.txt\n" +
            "names = custom/classes.names\nbackup = custom/backup' > custom/obj.data")
        print(self.images_list)

    def load(self):
        self.file.write("\n".join(self.images_list))
        self.file.close()

    def generate(self):
        os.system(
            "./darknet/darknet detector train custom/obj.data custom/yolov3-custom.cfg darknet/darknet -dont_show"
        )


cus = Customizer("custom/images", "custom/train.txt")
cus.load()
cus.generate()
