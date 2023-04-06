import logging
logging.basicConfig(filename = 'AppLog.txt',level = logging.DEBUG, format = '%(levelname)s %(name)s %(message)s')
import threading
from kivy.clock import Clock, mainthread
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton, MDRoundFlatButton
from kivy.properties import ListProperty
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.core.window import Window
from plyer import filechooser
from PIL import Image
from kivy.animation import Animation
from instabot import Bot
from kivy.config import Config
#from android.permissions import request_permissions, Permission
import instaloader
import time
import os
import shutil

Config.set('kivy', 'exit_on_escape', '0')
LabelBase.register(name="DancingScript", fn_regular="DancingScript-Regular.otf")
screen_helper = """

ScreenManager:
    MenuScreen:
    DownloadScreen:
    UploadScreen:

<MenuScreen>:
    name: 'menu'
    Image:
        source : "logo.jpg"
        pos_hint : {"x":0,"y":.8}
        size_hint : (.98,.20)
    MDLabel:
        text : "Instagram  profile  DP  downloader"
        halign : "center" 
        pos_hint : {'x':0,'y':.2}
        font_size: 70
        theme_text_color : "Custom"
        text_color : "#C6DEFF"
        font_name : "DancingScript"
    MDLabel:
        text : "&"
        halign : "center" 
        pos_hint : {'x':0,'y':.15}
        theme_text_color : "Custom"
        text_color : "#C6DEFF"
        font_name : "DancingScript"
        font_size : 70
    MDLabel:
        text : "Post  Uploader"
        halign : "center" 
        pos_hint : {'x':0,'y':.1}
        theme_text_color : "Custom"
        text_color : "#C6DEFF"
        font_name : "DancingScript"
        font_size : 70
    MDFillRoundFlatButton:
        text: 'Dp Download'
        font_name : "DancingScript"
        font_size:'30sp'
        theme_text_color: "Custom"
        text_color: "black"
        md_bg_color: "#707070"
        pos_hint : {"x":.22,"y":.33}
        size_hint : (.58, .1)
        on_press: 
            root.manager.current = 'profile'
            root.manager.transition.direction = 'left'
    MDFillRoundFlatButton:
        text: 'Post Upload'
        font_name : "DancingScript"
        font_size:'30sp'
        theme_text_color: "Custom"
        text_color: "black"
        md_bg_color: "#707070"
        size_hint : (.58, .1)
        pos_hint : {'x':.22,'y':.21}
        on_press: 
            root.manager.current = 'upload'
            root.manager.transition.direction = 'right'

<DownloadScreen>:
    name: 'profile'
    username : dp_name
    spinner : spinner
    btn_down : btn_down
    wait : waitt
    MDLabel:
        text: 'Dp Download'
        halign: 'center'
        theme_text_color : "Custom"
        text_color : "#C6DEFF"
        font_name : 'DancingScript'
        pos_hint : {'x':0,'y':.45}
        font_size : 70

    MDTextField:
        id : dp_name
        pos_hint : {'x':.15,'y':.8}
        size_hint : (.7, None)
        height: 50
        hint_text: 'Username'
        multiline: False
        icon_left: "account"

    MDRaisedButton:
        id : btn_down
        size_hint : (.35, .1)
        text: "Download"
        theme_text_color: "Custom"
        font_size:'20sp'
        text_color: "black"
        md_bg_color: "#707070"
        pos_hint : {'x':.31,'y':.62}
        on_press : 
            root.spinner_toggle()
            root.on_click1()
            root.spinner_toggle()
        disabled: True if dp_name.text == '' else False

    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: False

    Button:
        text: 'a'
        size_hint: (-1,-1)
        background_color : 0,0,0,1
        color : 'black'
        on_release: root.spinner_toggle()

    MDLabel:
        size_hint : (.97, .55)
        pos_hint : {'center_x': .5, 'center_y': .5}
        id: waitt
        font_size : 20
        color: 'black'
        ii: ''
        text: self.ii
        halign : "center"
        text_color : "#C6DEFF"
        font_name : "DancingScript"

<UploadScreen>:
    name: 'upload'
    user_name : post_name
    password : pswd
    caption : caption
    b_t: b_t
    b_t1 : b_t1
    wait : waitt
    image_btn : img_btn
    post : post_upload
    MDLabel:
        text: 'Post Upload'
        halign: 'center'
        theme_text_color : "Custom"
        text_color : "#C6DEFF"
        font_name : "DancingScript"
        pos_hint : {'x':0,'y':.45}
        font_size : 70

    MDTextField:
        size_hint : (.71, None)
        pos_hint : {'x':.13,'y':.8}
        height: '50dp'
        id : post_name
        hint_text: 'Username'
        icon_left: "account"
        multiline: False

    MDTextField:
        size_hint : (.71,None)
        pos_hint : {'x':.13,'y':.7}
        height: 70
        id : pswd
        password : True
        icon_left: "lock-outline"
        hint_text: 'Password'
        multiline: False

    MDIconButton:
        icon: "eye-off"
        pos_hint: {'x':.76,'y':.71}
        theme_text_color: "Hint"
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            pswd.password = False if pswd.password is True else True

    MDTextField:
        size_hint : (.71,None)
        pos_hint : {'x':.13,'y':.6}
        height: 70
        id : caption
        icon_left: "message-text"
        hint_text: 'Caption'
        multiline: True

    MDRaisedButton:
        id : post_upload
        size_hint : (.35, .1)
        text: " Post Upload"
        theme_text_color: "Custom"
        text_color: "black"
        font_size:'20sp'
        md_bg_color: "#707070"
        pos_hint : {'x':.52,'y':.42}
        on_release :
            root.spinner_toggle() 
            root.on_click1()
            root.spinner_toggle()
        disabled: True if post_name.text == '' or pswd.text == '' else False

    MDRaisedButton:
        id : img_btn
        size_hint : (.35, .1)
        pos_hint : {'x':.13,'y':.42}
        theme_text_color: "Custom"
        text_color: "black"
        font_size:'20sp'
        md_bg_color: "#707070"
        text : 'Select Image'
        disabled: True if post_name.text == '' or pswd.text == '' else False
        on_release: root.choose()

    MDLabel:
        size_hint : (.97, .65)
        id: b_t
        font_size : 30
        text_color : "#C6DEFF"
        font_name : "DancingScript"
        ii: 'Image Not selected'
        text: self.ii
        halign : "center"
        
    MDLabel:
        size_hint : (.97, .05)
        id: b_t1
        font_size : 30
        text_color : "#C6DEFF"
        font_name : "DancingScript"
        ii: ''
        text: self.ii
        halign : "center"
        
    Button:
        text: 'a'
        size_hint: (0,1)
        background_color : 0,0,0,1
        color : 'black'
        on_release: root.spinner_toggle()

    MDLabel:
        size_hint : (.97, .55)
        id: waitt
        font_size : 20
        color: 'black'
        text_color : "#C6DEFF"
        font_name : "DancingScript"
        ii: ''
        text: self.ii
        halign : "center"

"""


class MenuScreen(Screen):
    logging.info("In menuscreen")
    pass

class DownloadScreen(Screen):
    logging.info("In dp downdload Screen.")
    dialog = None
    username = ObjectProperty(None)
    btn_down = ObjectProperty(None)

    def spinner_toggle(self):
        logging.info("Into the spinner_toggle method which basically display the downloading while dp is downloading.")
        self.wait.ii = "Downloading..."
        self.wait.font_size = 70
        self.username.disabled = True
        self.btn_down.disabled = True

    @mainthread
    def on_click(self):
        try:
            dp = self.username.text
            logging.info(f'The Entered username is {dp}.')
            ig = instaloader.Instaloader()
            ig.download_profile(dp, profile_pic_only=True)
            #Apk code
            # path = '/storage/emulated/0/Download/' + dp
            # if os.path.exists(path):
            #     logging.info('dp already exists in the system')
            #     toast("Already exists", False)
            # else:
            #     os.mkdir(path)
            #     src_dir = '/data/user/0/org.test.insta_dp_post/files/app/' + dp
            #     time.sleep(10)
            #     dest_dir = path
            #
            #     allfiles = os.listdir(src_dir)
            #
            #     for fname in allfiles:
            #         shutil.copy2(os.path.join(src_dir, fname), dest_dir)
            toast("Downloaded!!")
            logging.info("Dp downloaded in the download folder")

        except instaloader.exceptions.ProfileNotExistsException:
            logging.warning('profile not exists')
            toast("Profile Not Exists")

        except Exception as e:
            logging.exception(e)

        except :
            logging.exception("Something went wrong")
            if not self.dialog:
                logging.error('f Error :- {e} ')
                self.dialog = MDDialog(text="Something Went Wrong", radius=[20, 7, 20, 7], auto_dismiss=False,
                                       buttons=[MDRoundFlatButton(text='Close', on_press=self.close_dialog)])
            self.dialog.open()
        self.wait.ii = ""
        self.username.text = ""
        self.username.disabled = False
        self.btn_down.disabled = False

    def close_dialog(self, obj):
        logging.info('Dialog box closed')
        self.dialog.dismiss()

    def on_click1(self):
        self.spinner_toggle()
        threading.Thread(target=(self.on_click)).start()

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = 'menu'
            self.parent.transition.direction = 'right'
            return True

class UploadScreen(Screen):
    logging.info("In class postUpload.")
    user_name = ObjectProperty(None)
    password = ObjectProperty(None)
    caption = ObjectProperty(None)
    post = ObjectProperty(None)
    image_btn = ObjectProperty(None)
    selection = ListProperty([])

    def choose(self):
        logging.info("Image Selecting....")
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        self.selection = selection

    def on_selection(self, *a, **k):
        logging.info("Image selected")
        self.b_t.ii = self.selection[0]

    def spinner_toggle(self):
        logging.info("Into the spinner_toggle method which basically display the Uploading while post gets uploaded.")
        self.wait.ii = "Uploading..."
        self.wait.font_size = 70
        self.user_name.disabled = True
        self.password.disabled = True
        self.caption.disabled = True
        self.post.disabled = True
        self.image_btn.disabled = True

    @mainthread
    def on_click(self):
        logging.info("Displaying Two Factor Authentication to be turned off")
        self.b_t1.ii = "Two Factor Authentication Needed to be turned off if in case its on!"
        anim = Animation(font_size=20)
        anim.start(self.b_t1)
        anim.repeat = True
        loc = '/data/data/org.test.insta_dp_post/files/app/config'
        api_loc = '/data/user/0/org.test.insta_dp_post/files/app/api.pyc'
        api_photo = '/data/user/0/org.test.insta_dp_post/files/app/api_photo.pyc'
        try:
            if os.path.exists(loc):
                shutil.rmtree('/data/data/org.test.insta_dp_post/files/app/config', ignore_errors=True) #Apk code

            if os.path.exists(api_loc):
                os.remove(
                    '/data/user/0/org.test.insta_dp_post/files/app/_python_bundle/site-packages/instabot/api/api.pyc')
                shutil.move('/data/user/0/org.test.insta_dp_post/files/app/api.pyc',
                            '/data/user/0/org.test.insta_dp_post/files/app/_python_bundle/site-packages/instabot/api/api.pyc') #Apk code

            if os.path.exists(api_photo):
                os.remove(
                    '/data/user/0/org.test.insta_dp_post/files/app/_python_bundle/site-packages/instabot/api/api_photo.pyc')
                shutil.move('/data/user/0/org.test.insta_dp_post/files/app/api_photo.pyc',
                            '/data/user/0/org.test.insta_dp_post/files/app/_python_bundle/site-packages/instabot/api/api_photo.pyc') #Apk code

            text = self.user_name.text
            logging.info("Entered username is {text}")

            txt2 = self.password.text
            logging.info("Entered password is {text2}")

            txt3 = self.caption.text
            logging.info("Entered caption is {text3}")

            path = self.b_t.ii
            logging.info("path {path}")

            img = path
            logging.info("img {img}")
            str1 = ""
            converted_img1 = str1.join(img)
            replaced_img = converted_img1.replace("\\", "/")
            # print("Converted :- ", converted_img1)
            # print("Converted :- ", replaced_img[-3:])
            extension = replaced_img[-3:]
            logging.info("Checking image extension")
            if extension == 'png' or extension == 'eic':
                logging.info("Image has png or heic extension so it will converted to jpg")
                img_png = Image.open(replaced_img)
                rgb_im = img_png.convert('RGB')
                rgb_im.save('modified_img.jpg')
                logging.info("Image was in png format which is  not supported so converted it in jpg and saved that image")

                im = Image.open('modified_img.jpg')
                im = im.resize((1080, 1080))
                im.save('modified_img.jpg')
                im.thumbnail((1080, 1080))
                im.save("modified_img.jpg")
                logging.info("Instagram has some size ration so image is converted into 1080*1080")
                bot = Bot()

                bot.login(username=text, password=txt2)
                logging.info("Logging successfull")
                #bot.upload_photo('/data/user/0/org.test.insta_dp_post/files/app/modified_img.jpg', caption=txt3) #Apk code
                bot.upload_photo('modified_img.jpg', caption=txt3)
                toast("photo uploaded!!")
                logging.info("Post uploaded")

            else:
                logging.info("image has jpg extension")
                im = Image.open(replaced_img)
                im1 = im.resize((1080, 1080))
                im1.save('Replaced_img1.jpg')
                im1.thumbnail((1080, 1080))
                im1.save("Replaced_img1.jpg")
                logging.info("Instagram has some size ration so image is converted into 1080*1080")
                bot = Bot()

                bot.login(username=text, password=txt2)
                logging.info("Logging successfull")
                #bot.upload_photo('/data/user/0/org.test.insta_dp_post/files/app/Replaced_img1.jpg', caption=txt3) #Apk code
                bot.upload_photo('Replaced_img1.jpg', caption=txt3)
                toast("photo uploaded!!")
                logging.info("Post uploaded")

        except Exception as e:
            logging.exception(f"Erorr {e}")

        except:
            logging.error("Displaying dialog box of somethhing went wrong")
            self.dialog = MDDialog(text="Something went wrong...", radius=[20, 7, 20, 7], auto_dismiss=False,
                                   buttons=[MDRoundFlatButton(text='Close', on_release=self.close_dialogg)]
                                   )
            self.dialog.open()

        self.user_name.text = ""
        self.password.text = ""
        self.caption.text = ""
        self.b_t.ii = "Image Not selected"
        self.wait.ii = ""
        self.user_name.disabled = False
        self.password.disabled = False
        self.caption.disabled = False
        self.post.disabled = False
        self.image_btn.disabled = False

    def close_dialogg(self, obj):
        logging.info("Dialogbox closed")
        self.dialog.dismiss()

    def on_click1(self):
        self.spinner_toggle()
        threading.Thread(target=(self.on_click())).start()

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = 'menu'
            self.parent.transition.direction = 'left'
            return True


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(DownloadScreen(name='profile'))
sm.add_widget(UploadScreen(name='upload'))


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        # request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA,
        #                      Permission.INTERNET, Permission.READ_MEDIA_IMAGES, Permission.ACCESS_FINE_LOCATION
        #                      ])
        return screen


DemoApp().run()
