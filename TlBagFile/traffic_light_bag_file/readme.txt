pip3 install pandas
python xml_to_csv.py should generate "traffic_light_labels.csv"
jupyter notebook
run split labels.ipynb will generate "train_labels.csv" and "test_labels.csv"
create "./output/tlbagtrainrecord" directory
python generate_tfrecord.py --csv_input=train_labels.csv  --output_path=output/tlbagtrainrecord/train.record
python generate_tfrecord.py --csv_input=test_labels.csv  --output_path=output/tlbagtrainrecord/test.record