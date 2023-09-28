datacrawler.py => crawl data từ file csv
htmltag_cleaner.py => bỏ html tag (hàm test)
stopwords_preprocessr.py => bỏ stopwords (test)
PickFileDialogGUI.py => hàm chọn file

1. Mở 1 thư mục của 1 nhãn chứa các file html
+> Copy 2 file vietnamese-stopwords.txt và preprocess.py vào
+> preprocess.py =>loại bỏ htmltag và stopwords
=> tạo ra 1 thư mục các file .txt xử lý lần 1

2. Cut các thư mục txt vào 1 thư mục riêng 
=> Thư mục [data_xử lý 1]: gồm 16 thư mục của các nhãn, mỗi thư mục là các file .txt
+> Copy rarewords_statistic.py vào thư mục đó
+> rarewords_statistic => thống kê từ số lần xuất hiện các từ trong data
=> file words.txt liệt kê các từ có số lần xuất hiện > 50 lần

3. Copy rarewords_preprocess.py vào thư mục [data_xử lý 1] và chạy => bỏ các từ hiếm
* Chú ý: Sửa đường dẫn thư mục lưu trữ trong file ewords_preprocess.py

=> tạo ra 1 thư mục data_xử lý 2 các file .txt xử lý lần 2