
import os
import cv2
import wx
import test as t
import asciiTest as aT
import Filter_R as JD

def cv_to_wx_bitmap(cv_img, max_size=(400, 300)):
    if cv_img is None:
        return wx.Bitmap(max_size[0], max_size[1])
    #Convert BGR to RGB
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    try:
        bmp = wx.Bitmap.FromBuffer(w, h, rgb)
    except Exception:
        img = wx.Image(w, h)
        img.SetData(rgb.tobytes())
        bmp = wx.Bitmap(img)
    return bmp

def fit_image(img, max_w=400, max_h=300):
    if img is None:
        return None
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    if new_size[0] <= 0 or new_size[1] <= 0:
        return img
    return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)


class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Image Processor', size=(1000, 650))

        self.orig_image = None 
        self.edited_image = None

        self._build_ui()

    def _build_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Left Panel : Preview of Image
        preview_panel = wx.Panel(panel)
        preview_sizer = wx.BoxSizer(wx.VERTICAL)

        #Initialize with empty bitmaps to reserve space
        empty_bmp = wx.Bitmap(400, 300)
        self.bitmap_before = wx.StaticBitmap(preview_panel, bitmap=empty_bmp)
        self.bitmap_after = wx.StaticBitmap(preview_panel, bitmap=empty_bmp)

        preview_sizer.Add(wx.StaticText(preview_panel, label='Original'), 0, wx.ALIGN_CENTER | wx.TOP, 5)
        preview_sizer.Add(self.bitmap_before, 1, wx.EXPAND | wx.ALL, 5)
        preview_sizer.Add(wx.StaticText(preview_panel, label='Edited'), 0, wx.ALIGN_CENTER | wx.TOP, 5)
        preview_sizer.Add(self.bitmap_after, 1, wx.EXPAND | wx.ALL, 5)

        preview_panel.SetSizer(preview_sizer)

        main_sizer.Add(preview_panel, 3, wx.EXPAND | wx.ALL, 8)

        #Right Panel : Image Control
        ctrl_panel = wx.Panel(panel, style=wx.BORDER_SIMPLE)
        ctrl_sizer = wx.BoxSizer(wx.VERTICAL)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        open_btn = wx.Button(ctrl_panel, label='Open')
        save_btn = wx.Button(ctrl_panel, label='Save')
        reset_btn = wx.Button(ctrl_panel, label='Reset')
        btn_sizer.Add(open_btn, 1, wx.EXPAND | wx.RIGHT, 4)
        btn_sizer.Add(save_btn, 1, wx.EXPAND | wx.RIGHT, 4)
        btn_sizer.Add(reset_btn, 1, wx.EXPAND)

        ctrl_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 8)

        # Effects dropdown
        ctrl_sizer.Add(wx.StaticText(ctrl_panel, label='Effect:'), 0, wx.LEFT | wx.TOP, 6)

        effect = [
            'None','Negative','Cartoonify','Ascii','Sepia','Oil Paint','Sketch','Black & White'
        ]
        self.effect_choice = wx.Choice(ctrl_panel, choices=effect)
        self.effect_choice.SetSelection(0)
        ctrl_sizer.Add(self.effect_choice, 0, wx.EXPAND | wx.ALL, 6)

        # Intensity Slider
        self.intensity_label = wx.StaticText(ctrl_panel, label='Intensity: 50')
        self.intensity_slider = wx.Slider(ctrl_panel, value=50, minValue=0, maxValue=100)

        ctrl_sizer.Add(self.intensity_label, 0, wx.LEFT | wx.TOP, 6)
        ctrl_sizer.Add(self.intensity_slider, 0, wx.EXPAND | wx.ALL, 6)

        
        apply_btn = wx.Button(ctrl_panel, label='Apply Effect')
        
        save_desktop_btn = wx.Button(ctrl_panel, label='Save to Desktop')

        ctrl_sizer.Add(apply_btn, 0, wx.EXPAND | wx.ALL, 6)
        
        ctrl_sizer.Add(save_desktop_btn, 0, wx.EXPAND | wx.ALL, 6)

        ctrl_sizer.AddStretchSpacer(1)

        ctrl_panel.SetSizer(ctrl_sizer)

        main_sizer.Add(ctrl_panel, 1, wx.EXPAND | wx.ALL, 8)
        panel.SetSizer(main_sizer)

        #Bind events
        open_btn.Bind(wx.EVT_BUTTON, self.on_open)
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        reset_btn.Bind(wx.EVT_BUTTON, self.on_reset)
        apply_btn.Bind(wx.EVT_BUTTON, self.on_apply)
        save_desktop_btn.Bind(wx.EVT_BUTTON, self.on_save_desktop)
        self.intensity_slider.Bind(wx.EVT_SLIDER, self.on_intensity_change)

   
    def load_image(self, path):
        img = cv2.imread(path)
        if img is None:
            wx.MessageBox('Could not read image.', 'Error')
            return
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self.orig_image = img.copy()
        self.edited_image = img.copy()
        self.update_previews()

    def update_previews(self):
        if self.orig_image is None:
            return
        before = fit_image(self.orig_image)
        after = fit_image(self.edited_image)
        if before is not None:
            self.bitmap_before.SetBitmap(cv_to_wx_bitmap(before))
        if after is not None:
            self.bitmap_after.SetBitmap(cv_to_wx_bitmap(after))
        self.Refresh()

    def on_open(self, event):
        with wx.FileDialog(self, 'Open Image', wildcard='Image files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp', style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fd:
            if fd.ShowModal() == wx.ID_OK:
                self.load_image(fd.GetPath())

    def on_save(self, event):
        if self.edited_image is None:
            wx.MessageBox('Nothing to save.', 'Info')
            return
        with wx.FileDialog(self, 'Save Image', wildcard='PNG (*.png)|*.png|JPEG (*.jpg)|*.jpg', style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fd:
            if fd.ShowModal() == wx.ID_OK:
                path = fd.GetPath()
                # Use extension to pick format
                ext = os.path.splitext(path)[1].lower()
                cv2.imwrite(path, self.edited_image)
                wx.MessageBox('Saved!', 'Info')

    def on_save_desktop(self, event):
        if self.edited_image is None:
            wx.MessageBox('Nothing to save.', 'Info')
            return
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.isdir(desktop):
            desktop = os.path.expanduser('~')
        path = os.path.join(desktop, 'edited_image.png')
        base, ext = os.path.splitext(path)
        n = 1
        while os.path.exists(path):
            path = f"{base}_{n}{ext}"
            n += 1
        cv2.imwrite(path, self.edited_image)
        wx.MessageBox(f'Saved to {path}', 'Info')

    def on_reset(self, event):
        if self.orig_image is not None:
            self.edited_image = self.orig_image.copy()
            self.update_previews()


    def on_intensity_change(self, event):
        val = self.intensity_slider.GetValue()
        self.intensity_label.SetLabel(f'Intensity: {val}')

    #Effects Edits
    def on_apply(self, event):
        if self.orig_image is None:
            wx.MessageBox('Load an image first.', 'Info')
            return

        img = self.orig_image.copy()
        intensity = self.intensity_slider.GetValue() / 50.0
        f = self.effect_choice.GetStringSelection()

        try:
            if f== 'None':
                result = img
            elif f == "Cartoonify":
                result = t.cartoonify(img,intensity)

            elif f == 'Ascii':
                import numpy as np
                from PIL import Image
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                ascii_pil = aT.image_to_ascii(pil_img)
                result = cv2.cvtColor(np.array(ascii_pil), cv2.COLOR_RGB2BGR)
                
            elif f == 'Negative':
                result=JD.negative_filter(img)
            elif f== 'Oil Paint':
                result=JD.oil_paint_effect_fast(img)
            elif f == 'Sepia':
                result=JD.sepia_filter(img)

            elif f == 'Sketch':
                result =t.sketch_filter(img,intensity)
            elif f == 'Black & White':
                result =t.Black_White(img,intensity)
                
            else:
                result = img

            # Ensure result is BGR 3-channel
            if len(result.shape) == 2:
                result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

            self.edited_image = result
            self.update_previews()
        except Exception as e:
            wx.MessageBox(f'Error applying filter: {e}', 'Error')
        

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

        
