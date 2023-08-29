import os
import pandas as pd

def filter_labels(label_list, label_root, root_save, dir_name, conf_threshold=0.6):
    save_dir_format = os.path.join(root_save, dir_name, r"labels_{conf_threshold}")
    save_path = os.path.join(root_save, dir_name)
    for label_name in label_list:
        label_path = os.path.join(label_root, label_name)
        df = pd.read_csv(label_path, sep=r'\s+', header=None)
        save_dir = save_dir_format.format(conf_threshold=conf_threshold)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        if not os.path.exists(save_dir):
            #print(save_dir)
            os.mkdir(save_dir)
        save_label = os.path.join(save_dir, label_name)
        df_filter = df[df.iloc[:, 5] >= conf_threshold].iloc[:, :5]
        df_filter.to_csv(save_label, header=False, index=False, sep=' ')

if __name__ == "__main__":
    root_read = r"/home/zhaogan/yolov5-6.1/runs/detect"
    root_save = r"/home/zhaogan/yolov5-6.1/runs/filter"
    type_list = ['train', 'val']
    threshold_list = [0.2]
    dir_path = os.listdir(root_read)
    for dir_name in dir_path:
        if 'fx' in dir_name:

            label_root = os.path.join(root_read, dir_name, "labels")

            label_list = os.listdir(label_root)
            for threshold in threshold_list:
                filter_labels(label_list=label_list, label_root=label_root, root_save=root_save, dir_name=dir_name, conf_threshold=threshold)

            