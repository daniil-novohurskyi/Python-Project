import pandas as pd
def walk_dir_read(start_dir):
    all_df = pd.DataFrame()
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
                all_df = pd.concat([all_df, df], left_index=True, right_index=True)
    return all_df