from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation
import json
import os

Window.clearcolor = (0.05, 0.05, 0.08, 1)

class Novel:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

class NovelStorage:
    def __init__(self):
        self.filename = 'novels.json'
        self.novels = self.load_novels()
    
    def load_novels(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Novel(n['title'], n['author'], n['content']) for n in data]
            except:
                return self.get_sample_novels()
        return self.get_sample_novels()
    
    def get_sample_novels(self):
        return [
            Novel("별빛 아래서", "김작가", "밤하늘의 별을 바라보며 나는 생각했다.\n\n그 빛이 수백 년 전의 것이라는 사실을...\n\n우리가 보는 모든 것은 과거의 기억일 뿐이다."),
            Novel("도시의 밤", "이작가", "네온사인이 반짝이는 거리.\n\n수많은 사람들이 지나가지만\n\n모두가 외로워 보였다."),
            Novel("첫눈", "박작가", "창밖으로 하얀 눈이 내린다.\n\n올해의 첫눈.\n\n당신과 함께 보고 싶었다.")
        ]
    
    def save_novels(self):
        data = [{'title': n.title, 'author': n.author, 'content': n.content} for n in self.novels]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_novel(self, novel):
        self.novels.insert(0, novel)
        self.save_novels()

class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            self.bg_color = Color(0.15, 0.15, 0.2, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class PrimaryButton(ModernButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color.rgba = (0.4, 0.35, 0.85, 1)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = NovelStorage()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        header = BoxLayout(size_hint_y=0.12, spacing=15)
        title_label = Label(
            text='Stories',
            font_size='32sp',
            bold=True,
            color=(1, 1, 1, 1),
            font_name='Roboto'
        )
        write_btn = PrimaryButton(
            text='Write',
            size_hint_x=0.25,
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        write_btn.bind(on_press=self.go_to_write)
        header.add_widget(title_label)
        header.add_widget(write_btn)
        
        scroll = ScrollView()
        self.novels_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        self.novels_layout.bind(minimum_height=self.novels_layout.setter('height'))
        
        self.refresh_novels()
        
        scroll.add_widget(self.novels_layout)
        layout.add_widget(header)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def refresh_novels(self):
        self.novels_layout.clear_widgets()
        self.storage.novels = self.storage.load_novels()
        
        for novel in self.storage.novels:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=140,
                padding=20,
                spacing=8
            )
            
            with card.canvas.before:
                Color(0.12, 0.12, 0.16, 1)
                card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[16])
                card.bind(pos=lambda x, y, rect=card.rect: setattr(rect, 'pos', x.pos))
                card.bind(size=lambda x, y, rect=card.rect: setattr(rect, 'size', x.size))
            
            title_label = Label(
                text=novel.title,
                font_size='22sp',
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_y=0.35,
                halign='left',
                valign='middle'
            )
            title_label.bind(size=title_label.setter('text_size'))
            
            author_label = Label(
                text=novel.author,
                font_size='14sp',
                color=(0.6, 0.6, 0.7, 1),
                size_hint_y=0.25,
                halign='left',
                valign='middle'
            )
            author_label.bind(size=author_label.setter('text_size'))
            
            preview = novel.content[:40] + '...' if len(novel.content) > 40 else novel.content
            preview = preview.replace('\n', ' ')
            content_label = Label(
                text=preview,
                font_size='13sp',
                color=(0.5, 0.5, 0.6, 1),
                size_hint_y=0.25,
                halign='left',
                valign='middle'
            )
            content_label.bind(size=content_label.setter('text_size'))
            
            btn_layout = BoxLayout(size_hint_y=0.15)
            btn = Button(
                text='Read',
                size_hint_x=0.3,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=(0.6, 0.55, 1, 1),
                font_size='14sp'
            )
            btn.bind(on_press=lambda x, n=novel: self.read_novel(n))
            btn_layout.add_widget(Label())
            btn_layout.add_widget(btn)
            
            card.add_widget(title_label)
            card.add_widget(author_label)
            card.add_widget(content_label)
            card.add_widget(btn_layout)
            
            self.novels_layout.add_widget(card)
    
    def go_to_write(self, instance):
        self.manager.current = 'write'
    
    def read_novel(self, novel):
        read_screen = self.manager.get_screen('read')
        read_screen.display_novel(novel)
        self.manager.current = 'read'

class WriteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = BoxLayout(size_hint_y=0.1, spacing=15)
        back_btn = ModernButton(
            text='← Back',
            size_hint_x=0.25,
            color=(0.7, 0.7, 0.8, 1),
            font_size='15sp'
        )
        back_btn.bind(on_press=self.go_back)
        title_label = Label(
            text='New Story',
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        header.add_widget(back_btn)
        header.add_widget(title_label)
        
        self.title_input = TextInput(
            hint_text='Title',
            size_hint_y=0.08,
            multiline=False,
            font_size='18sp',
            background_color=(0.12, 0.12, 0.16, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            cursor_color=(0.6, 0.55, 1, 1),
            padding=[15, 12]
        )
        
        self.author_input = TextInput(
            hint_text='Author',
            size_hint_y=0.08,
            multiline=False,
            font_size='16sp',
            background_color=(0.12, 0.12, 0.16, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            cursor_color=(0.6, 0.55, 1, 1),
            padding=[15, 12]
        )
        
        self.content_input = TextInput(
            hint_text='Start writing your story...',
            multiline=True,
            font_size='16sp',
            background_color=(0.12, 0.12, 0.16, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            cursor_color=(0.6, 0.55, 1, 1),
            padding=[15, 15]
        )
        
        save_btn = PrimaryButton(
            text='Publish',
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            font_size='17sp',
            bold=True
        )
        save_btn.bind(on_press=self.save_novel)
        
        layout.add_widget(header)
        layout.add_widget(self.title_input)
        layout.add_widget(self.author_input)
        layout.add_widget(self.content_input)
        layout.add_widget(save_btn)
        self.add_widget(layout)
    
    def save_novel(self, instance):
        title = self.title_input.text.strip()
        author = self.author_input.text.strip()
        content = self.content_input.text.strip()
        
        if title and author and content:
            home_screen = self.manager.get_screen('home')
            novel = Novel(title, author, content)
            home_screen.storage.add_novel(novel)
            home_screen.refresh_novels()
            
            self.title_input.text = ''
            self.author_input.text = ''
            self.content_input.text = ''
            
            self.manager.current = 'home'
    
    def go_back(self, instance):
        self.manager.current = 'home'

class ReadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = BoxLayout(size_hint_y=0.08, spacing=15)
        back_btn = ModernButton(
            text='← Back',
            size_hint_x=0.25,
            color=(0.7, 0.7, 0.8, 1),
            font_size='15sp'
        )
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        header.add_widget(Label(text=''))
        
        self.title_label = Label(
            text='',
            font_size='28sp',
            bold=True,
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        
        self.author_label = Label(
            text='',
            font_size='15sp',
            size_hint_y=0.05,
            color=(0.6, 0.6, 0.7, 1),
            halign='left',
            valign='middle'
        )
        self.author_label.bind(size=self.author_label.setter('text_size'))
        
        separator = BoxLayout(size_hint_y=0.005)
        with separator.canvas:
            Color(0.2, 0.2, 0.25, 1)
            separator.line = Line(points=[0, 0, 100, 0], width=1)
        separator.bind(pos=self.update_line, size=self.update_line)
        
        scroll = ScrollView()
        self.content_label = Label(
            text='',
            font_size='17sp',
            size_hint_y=None,
            color=(0.85, 0.85, 0.9, 1),
            halign='left',
            valign='top',
            padding=(5, 20),
            line_height=1.5
        )
        self.content_label.bind(
            texture_size=self.content_label.setter('size'),
            size=self.content_label.setter('text_size')
        )
        scroll.add_widget(self.content_label)
        
        layout.add_widget(header)
        layout.add_widget(self.title_label)
        layout.add_widget(self.author_label)
        layout.add_widget(separator)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def update_line(self, instance, value):
        instance.line.points = [instance.x, instance.y, instance.right, instance.y]
    
    def display_novel(self, novel):
        self.title_label.text = novel.title
        self.author_label.text = f'by {novel.author}'
        self.content_label.text = novel.content
    
    def go_back(self, instance):
        self.manager.current = 'home'

class NovelApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=0.2))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(WriteScreen(name='write'))
        sm.add_widget(ReadScreen(name='read'))
        return sm

if __name__ == '__main__':
    NovelApp().run()
