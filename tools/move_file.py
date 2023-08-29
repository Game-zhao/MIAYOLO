import os
import shutil

def copyto(path, filename_list, dst_path):
    num_file = len(filename_list)
    current_num_file = 0
    for filepath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.jpg') and filename.split(".")[0] in filename_list:
                src_file = os.path.join(filepath, filename)
                dst_file = os.path.join(dst_path, filename)
                if not os.path.exists(dst_file):
                    shutil.copy(src_file, dst_file)
                    print(src_file,'========>', dst_file)
                current_num_file += 1
        if current_num_file >= num_file:
            break
            

if __name__ == '__main__':
    # print("running")
    annotation_path = r"I:\data_to_train\newData\data\Annotations_"
    annotation_list = os.listdir(annotation_path)
    filename_list = [x.split(".")[0] for x in annotation_list]
    src_path = r'H:\dataToCheck\original_images'     #绝对路径
    dst_path = r"I:\data_to_train\newData\data\JPEGImages_"
    copyto(src_path, filename_list, dst_path)