from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import requests
import json

# Supabase 설정
SUPABASE_URL = "https://ikhjpmtstqhykviedghn.supabase.co"
SUPABASE_KEY = "sb_publishable_tVA9kKSGhT7UKqVTHbdsCA_ynflRRNU"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

Window.clearcolor = (0.05, 0.05, 0.1, 1)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 제목
        title = Label(
            text='Kiro',
            font_size='32sp',
            size_hint_y=0.15,
            color=(0.8, 0.6, 1, 1)
        )
        layout.add_widget(title)
        
        # 소설 목록 스크롤
        scroll = ScrollView(size_hint=(1, 0.7))
        self.novels_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.novels_layout.bind(minimum_height=self.novels_layout.setter('height'))
        scroll.add_widget(self.novels_layout)
        layout.add_widget(scroll)
        
        # 새로고침 버튼
        refresh_btn = Button(
            text='새로고침',
            size_hint_y=0.08,
            background_color=(0.6, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        refresh_btn.bind(on_press=self.load_novels)
        layout.add_widget(refresh_btn)
        
        # 쓰기 버튼
        write_btn = Button(
            text='새 소설 쓰기',
            size_hint_y=0.08,
            background_color=(0.8, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        write_btn.bind(on_press=self.go_to_write)
        layout.add_widget(write_btn)
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_novels()
    
    def load_novels(self, *args):
        self.novels_layout.clear_widgets()
        try:
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/novels?select=*&order=created_at.desc",
                headers=HEADERS
            )
            if response.status_code == 200:
                novels = response.json()
                if novels:
                    for novel in novels:
                        btn = Button(
                            text=f"{novel['title']}\n작가: {novel['author']} | 조회수: {novel['views']}",
                            size_hint_y=None,
                            height=80,
                            background_color=(0.15, 0.15, 0.25, 1),
                            color=(1, 1, 1, 1)
                        )
                        btn.bind(on_press=lambda x, n=novel: self.open_novel(n))
                        self.novels_layout.add_widget(btn)
                else:
                    self.novels_layout.add_widget(Label(
                        text='아직 소설이 없어요\n첫 번째 작가가 되어보세요!',
                        size_hint_y=None,
                        height=100,
                        color=(0.7, 0.7, 0.7, 1)
                    ))
            else:
                self.novels_layout.add_widget(Label(
                    text=f'불러오기 실패\n상태 코드: {response.status_code}',
                    size_hint_y=None,
                    height=100,
                    color=(1, 0.3, 0.3, 1)
                ))
        except Exception as e:
            self.novels_layout.add_widget(Label(
                text=f'오류 발생:\n{str(e)}',
                size_hint_y=None,
                height=100,
                color=(1, 0.3, 0.3, 1)
            ))
    
    def open_novel(self, novel):
        app = App.get_running_app()
        app.root.get_screen('read').display_novel(novel)
        app.root.current = 'read'
    
    def go_to_write(self, *args):
        App.get_running_app().root.current = 'write'

class WriteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 제목
        title_label = Label(
            text='새 소설 쓰기',
            font_size='24sp',
            size_hint_y=0.08,
            color=(0.8, 0.6, 1, 1)
        )
        layout.add_widget(title_label)
        
        # 작가 이름
        layout.add_widget(Label(text='작가 이름', size_hint_y=0.05, color=(0.9, 0.9, 0.9, 1)))
        self.author_input = TextInput(
            hint_text='당신의 필명을 입력하세요',
            size_hint_y=0.08,
            multiline=False,
            background_color=(0.2, 0.2, 0.3, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.author_input)
        
        # 소설 제목
        layout.add_widget(Label(text='제목', size_hint_y=0.05, color=(0.9, 0.9, 0.9, 1)))
        self.title_input = TextInput(
            hint_text='소설 제목',
            size_hint_y=0.08,
            multiline=False,
            background_color=(0.2, 0.2, 0.3, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.title_input)
        
        # 내용
        layout.add_widget(Label(text='내용', size_hint_y=0.05, color=(0.9, 0.9, 0.9, 1)))
        self.content_input = TextInput(
            hint_text='여기에 소설을 작성하세요...',
            size_hint_y=0.5,
            multiline=True,
            background_color=(0.2, 0.2, 0.3, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.content_input)
        
        # 버튼들
        btn_layout = BoxLayout(size_hint_y=0.08, spacing=10)
        
        cancel_btn = Button(
            text='취소',
            background_color=(0.4, 0.4, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        cancel_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(cancel_btn)
        
        save_btn = Button(
            text='업로드',
            background_color=(0.8, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        save_btn.bind(on_press=self.save_novel)
        btn_layout.add_widget(save_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def save_novel(self, *args):
        author = self.author_input.text.strip()
        title = self.title_input.text.strip()
        content = self.content_input.text.strip()
        
        if not author or not title or not content:
            return
        
        try:
            data = {
                "author": author,
                "title": title,
                "content": content,
                "views": 0
            }
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/novels",
                headers=HEADERS,
                json=data
            )
            if response.status_code == 201:
                self.author_input.text = ''
                self.title_input.text = ''
                self.content_input.text = ''
                App.get_running_app().root.current = 'home'
        except Exception as e:
            print(f"업로드 오류: {e}")
    
    def go_back(self, *args):
        App.get_running_app().root.current = 'home'

class ReadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.title_label = Label(
            text='',
            font_size='24sp',
            size_hint_y=0.1,
            color=(0.8, 0.6, 1, 1)
        )
        layout.add_widget(self.title_label)
        
        self.author_label = Label(
            text='',
            font_size='14sp',
            size_hint_y=0.05,
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.author_label)
        
        scroll = ScrollView(size_hint=(1, 0.75))
        self.content_label = Label(
            text='',
            font_size='16sp',
            size_hint_y=None,
            color=(0.95, 0.95, 0.95, 1),
            text_size=(Window.width - 60, None)
        )
        self.content_label.bind(texture_size=self.content_label.setter('size'))
        scroll.add_widget(self.content_label)
        layout.add_widget(scroll)
        
        back_btn = Button(
            text='목록으로',
            size_hint_y=0.08,
            background_color=(0.6, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        self.current_novel_id = None
    
    def display_novel(self, novel):
        self.current_novel_id = novel['id']
        self.title_label.text = novel['title']
        self.author_label.text = f"작가: {novel['author']} | 조회수: {novel['views']}"
        self.content_label.text = novel['content']
        
        # 조회수 증가
        try:
            requests.patch(
                f"{SUPABASE_URL}/rest/v1/novels?id=eq.{novel['id']}",
                headers=HEADERS,
                json={"views": novel['views'] + 1}
            )
        except:
            pass
    
    def go_back(self, *args):
        App.get_running_app().root.current = 'home'

class KiroApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(WriteScreen(name='write'))
        sm.add_widget(ReadScreen(name='read'))
        return sm

if __name__ == '__main__':
    KiroApp().run()
