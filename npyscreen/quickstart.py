import npyscreen
from npyscreen import (Form, TitleText, TitleFilename, TitleFilenameCombo,
    TitleDateCombo, TitleSliderPercent, MultiLineEdit, TitleSelectOne,
    TitleMultiSelect)
#npyscreen.disableColor()

class TestApp(npyscreen.NPSApp):
    def main(self):
        F  = Form(name="Welcome to Feihong's Npyscreen Example")
        self.t  = F.add(TitleText, name="Text:", )
        fn = F.add(TitleFilename, name="Filename:",)
        fn2 = F.add(TitleFilenameCombo, name="Filename2:")
        dt = F.add(TitleDateCombo, name="Date:")
        s  = F.add(TitleSliderPercent, accuracy=0, out_of=12, name="Slider")
        ml = F.add(MultiLineEdit,
               value = """try typing here!\nMutiline text, press ^R to reformat.\n""",
               max_height=5, rely=9)
        self.ms = F.add(TitleSelectOne, max_height=4, value = [1,], name="Pick One",
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        ms2 = F.add(TitleMultiSelect, max_height =-2, value = [1,], name="Pick Several",
                values = ["Option1","Option2","Option3"], scroll_exit=True)

        # This lets the user play with the Form.
        F.edit()

        # This won't get printed for some reason.
        print(self.t.value)

if __name__ == "__main__":
    app = TestApp()
    app.run()
    print(app.t.value)
    print(app.ms.get_selected_objects())
