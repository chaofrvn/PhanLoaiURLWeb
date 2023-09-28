from tkinter import *
import tkinter.messagebox as mbox
import requests
from bs4 import BeautifulSoup
import time

from services import *

BG_GRAY = "#3973ad"
BG_COLOR = "#ffffff"
TEXT_COLOR = "#000103"
SELECTED_COLOR = "#2a5b91"  
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 14"


categories = {'bat dong san': "Bất động sản/Nhà đất",
         'chinh tri': "Chính trị",
         'giai tri': "Giải trí",
         'giao duc': "Giáo dục",
         'khoa hoc': "Khoa học",
         'kinh doanh': "Kinh doanh",
         'phap luat': "Pháp luật",
         'suc khoe': "Sức khỏe",
         'the gioi': "Thế giới",
         'the thao': "Thể thao",
         'thuc pham': "Thực phẩm",
         'xe': "Xe cộ"}

algorithm_options = ["SVM", "Neural Networks", "KNN"]
feature_selection_options = ["None", "Mutual Information", "Chi-square", "ANOVA F"]
n_feature_options = ["None", 2500, 5000, 7500]


class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        # Setup window
        self.window.title("Phân loại trang Web")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=900, bg=BG_COLOR)

        self.input_frame = Frame(self.window, bg=BG_COLOR)
        self.input_frame.pack(side=TOP, padx=10, pady=10)

        # Thanh nhập URL
        self.url_label = Label(
            self.input_frame,
            text="URL:",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        
        self.url_label.pack(side=LEFT)

        self.url_entry = Entry(
            self.input_frame,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=FONT,
            width=40
        )
        
        self.url_entry.pack(side=LEFT, padx=10)

        self.submit_button = Button(
            self.input_frame,
            text="Submit",
            font=FONT_BOLD,
            width=10,
            bg=BG_GRAY,
            command=self._submit
        )
        self.submit_button.pack(side=LEFT)


        # Option Frames
        self.option_frame = Frame(self.window, bg=BG_COLOR)
        self.option_frame.pack(side=TOP, padx=10, pady=10)

        # Lựa chọn Loại chọn đặc trưng
        fs_label = Label(
            self.option_frame,
            text="Phương pháp chọn đặc trưng",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )

        fs_label.grid(row=0, column=1, padx=0, pady=0)
        
        self.feature_selection_var = StringVar()
        self.feature_selection_var.set("None")

        feature_selection_option_menu = OptionMenu(self.option_frame, self.feature_selection_var, *feature_selection_options)
        feature_selection_option_menu.config(width=20, font=('Helvetica', 14))
        feature_selection_option_menu.grid(row=1, column=1, padx=10, pady=10)

        # Lựa chọn số đặc trưng chọn lựa
        nf_label = Label(
            self.option_frame,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )

        nf_label.grid(row=0, column=1, padx=0, pady=0)
        
        self.n_feature_var = StringVar()
        self.n_feature_var.set("None")

        feature_selection_option_menu = OptionMenu(self.option_frame, self.n_feature_var, *n_feature_options)
        feature_selection_option_menu.config(width=20, font=('Helvetica', 14))
        feature_selection_option_menu.grid(row=1, column=1, padx=10, pady=10)


        

        # Lựa chọn thuật toán
        al_label = Label(
            self.option_frame,
            text="Lựa chọn thuật toán sử dụng",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )

        al_label.grid(row=0, column=1, padx=0, pady=0)
        
        
        self.algorithm_var = StringVar()
        self.algorithm_var.set("SVM")

        algorithm_option_menu = OptionMenu(self.option_frame, self.algorithm_var, *algorithm_options)
        algorithm_option_menu.config(width=20, font=('Helvetica', 14))
        algorithm_option_menu.grid(row=1, column=1, padx=10, pady=10)

        ##
        self.message_text = Text(
            self.window,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=FONT,
            height=12,
            state=DISABLED
        )
        self.message_text.pack(side=BOTTOM, fill=BOTH, padx=20, pady=20)


    def _submit(self):
        url = self.url_entry.get()

        self._update_message(">>> Url: {}".format(url))
        self._update_message(">>> Thuật toán sử dụng: {}".format(self.algorithm_var.get()))
        #self._update_message(">>> Phương pháp trích chọn đặc trưng: {}".format(self.feature_selection_var.get()))
        #self._update_message(">>> Số đặc trưng được lựa chọn: {}".format(self.n_feature_var.get()))

        #Đọc url
        status_read_url, soup, message = self._read_url(url)
        self.url_entry.delete(0, END)

        if status_read_url:
            self._update_message(">> Đọc dữ liệu từ url: {}".format(message))
            status_preprocess, vector , message = self._preprocess_data(soup)
            self._update_message(message)

            if status_preprocess:
                status_classification, result, message = self._classification(vector)
                self._update_message(message + "\n")
                if status_classification:

                    mbox.showinfo("Kết quả", "Nhãn của trang web là: " + result)
                else:
                    mbox.showerror("Đã xảy ra lỗi", "Phân loại không thành công!!!")
            else:
                mbox.showerror("Đã xảy ra lỗi", "Tiền xử lý dữ liệu vào không thành công!!!")
            
        else:
            self._update_message(">> Lỗi khi đọc url: {}".format(message))

    def _read_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            return True, soup, "Thành công"
        except Exception as e:
            return False, None, str(e)

    def _preprocess_data(self, soup):
        self._update_message(">> Tiền xử lý dữ liệu...")
        try:
            dt = htmltag_remove(soup)
            self._update_message("  > Loại bỏ html tag thành công")
        except:
            self._update_message("  > Loại bỏ html tag không thành công")
            return False, None, ">> Xử lý url không thành công, vui lòng thử với url khác"

        try:
            dt = special_character_remove(dt)
            self._update_message("  > Loại bỏ các ký tự đặc biệt thành công")
        except Exception as e:
            print(e)
            self._update_message("  > Loại bỏ các ký tự đặc biệt không thành công")
            return False, None, ">> Xử lý url không thành công, vui lòng thử với url khác"

        try:
            dt = stopwords_remove(dt)
            self._update_message("  > Loại bỏ stopwords thành công")
        except:
            self._update_message("  > Loại bỏ stopwords không thành công")
            return False, None, ">> Xử lý url không thành công, vui lòng thử với url khác"

        try:
            vector = create_bow_vector(dt)
            self._update_message("  > Khởi tạo vector số thành công")
        except:
            self._update_message("  > Khởi tạo vector số không thành công")
            return False, None, ">> Xử lý url không thành công, vui lòng thử với url khác"

        try:
            fs = self.feature_selection_var.get()
            nf = self.n_feature_var.get()
            vector = feature_select(vector, fs, nf)
            self._update_message("  > Chọn lựa đặc trưng thành công")
        except Exception as e:
            print(e)
            self._update_message("  > Chọn lựa đặc trưng không thành công")
            return False, None, ">> Xử lý url không thành công, vui lòng thử với url khác"
        
        return True, vector, ">> Tiền xử lý dữ liệu thành công"

    def _classification(self, vector):
        try:
            algorithm = self.algorithm_var.get()
            feature_selection = self.feature_selection_var.get()
            n_feature = self.n_feature_var.get()
            result = classification(vector, algorithm, feature_selection, n_feature)
            result = categories[result]
            return True, result, ">>> Nhãn của trang web này là: " + result
        except Exception as e:
            print(e)
            return False, None, ">>> Phân loại không thành công, vui lòng thử lại"
        

    def _update_message(self, message):
        self.message_text.config(state=NORMAL)
        self.message_text.insert(END, message + "\n")
        self.message_text.config(state=DISABLED)
        self.message_text.see(END)
        self.window.update()


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
