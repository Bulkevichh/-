
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
import os

# Задаём размер окна, как у стандартного мобильного телефона (360x640 пикселей)
Window.size = (360, 640)

# Определяем собственный тулбар на базе BoxLayout
class MyToolbar(BoxLayout):
    title = StringProperty("")

    def __init__(self, **kwargs):
        super(MyToolbar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '56dp'
        # Добавляем лейбл с заголовком
        self.add_widget(MDLabel(text=self.title, halign='center', theme_text_color='Primary'))

KV = '''
#:import dp kivy.metrics.dp
#:import FloatLayout kivy.uix.floatlayout.FloatLayout
#:import MDLabel kivymd.uix.label.MDLabel
#:import MDRaisedButton kivymd.uix.button.MDRaisedButton
#:import MDSlider kivymd.uix.slider.MDSlider
#:import MDBoxLayout kivymd.uix.boxlayout.MDBoxLayout

ScreenManager:
    SurveyScreen:
    MainScreen:
    DiaryScreen:
    EndSurveyScreen:

<SurveyScreen>:
    name: "survey"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)
        MDLabel:
            text: "Начальный опрос: Как вы себя чувствуете?"
            halign: "center"
            font_style: "H5"
        MDSlider:
            id: mood_slider
            min: 0
            max: 10
            value: 5
        MDRaisedButton:
            text: "Продолжить"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.initial_mood = mood_slider.value; \
                app.log_diary("Начальный опрос: " + str(mood_slider.value)); \
                root.manager.current = "main"

<MainScreen>:
    name: "main"
    FloatLayout:
        # UI слой (отвечает за кнопки и контролы)
        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            padding: dp(10)
            spacing: dp(10)
            # Верхняя панель с заголовком
            MyToolbar:
                title: "Дыхательные техники"
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: dp(200)
                spacing: dp(10)
                MDRaisedButton:
                    text: "Квадратное дыхание"
                    size_hint_x: 0.6
                    pos_hint: {"center_x": 0.5}
                    on_release: app.start_technique("Квадратное дыхание")
                MDRaisedButton:
                    text: "Дыхание Нади Шодхана"
                    size_hint_x: 0.6
                    pos_hint: {"center_x": 0.5}
                    on_release: app.start_technique("Дыхание Нади Шодхана")
                MDRaisedButton:
                    text: "Диафрагмальное дыхание"
                    size_hint_x: 0.6
                    pos_hint: {"center_x": 0.5}
                    on_release: app.start_technique("Диафрагмальное дыхание")
                MDRaisedButton:
                    text: "Дыхание 4-7-8"
                    size_hint_x: 0.6
                    pos_hint: {"center_x": 0.5}
                    on_release: app.start_technique("Дыхание 4-7-8")
            MDRaisedButton:
                text: "Дневник"
                size_hint: (None, None)
                size: dp(200), dp(48)
                pos_hint: {"center_x": 0.5, "y": 0.05}
                on_release: root.manager.current = "diary"

        # Animation слой – располагается поверх UI для отображения анимации
        FloatLayout:
            id: animation_layer
            size_hint: (1, 1)

<DiaryScreen>:
    name: "diary"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)
        padding: dp(10)
        MyToolbar:
            title: "Дневник"
        ScrollView:
            MDLabel:
                id: diary_label
                text: app.get_diary_entries()
                markup: True
                size_hint_y: None
                height: self.texture_size[1]
                padding: dp(10), dp(10)
        MDRaisedButton:
            text: "Назад"
            size_hint: (None, None)
            size: dp(200), dp(48)
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "main"

<EndSurveyScreen>:
    name: "endsurvey"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)
        MDLabel:
            text: "Заключительный опрос: Как вы себя чувствуете?"
            halign: "center"
            font_style: "H5"
        MDSlider:
            id: mood_slider_end
            min: 0
            max: 10
            value: 5
        MDRaisedButton:
            text: "Завершить"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.final_mood = mood_slider_end.value; \
                result = 'улучшилось' if app.final_mood > app.initial_mood else ('ухудшилось' if app.final_mood < app.initial_mood else 'без изменений'); \
                app.log_diary("Конечный опрос: " + str(mood_slider_end.value) + " - Состояние " + result); \
                root.manager.current = "diary"
'''

class SurveyScreen(MDScreen):
    pass

class MainScreen(MDScreen):
    pass

class DiaryScreen(MDScreen):
    pass

class EndSurveyScreen(MDScreen):
    pass

class CircleWidget(Widget):
    # Свойство размера круга будет меняться при анимации
    circle_size = NumericProperty(100)

    def __init__(self, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        with self.canvas:
            from kivy.graphics import Color, Ellipse
            Color(0, 0.5, 1, 1)  # лазурный цвет
            self.ellipse = Ellipse(pos=self.center, size=(self.circle_size, self.circle_size))
        self.bind(pos=self.update_circle, circle_size=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.ellipse.size = (self.circle_size, self.circle_size)
        self.ellipse.pos = (self.center_x - self.circle_size / 2, self.center_y - self.circle_size / 2)

class BreathingApp(MDApp):
    diary_file = "diary.txt"

    def build(self):
        # Загружаем записи дневника из файла, если он существует
        if os.path.exists(self.diary_file):
            with open(self.diary_file, "r", encoding="utf-8") as f:
                self.diary_entries = f.read().splitlines()
        else:
            self.diary_entries = []
        self.initial_mood = 5  # значение по умолчанию
        self.final_mood = 5
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        from kivy.factory import Factory
        Factory.register('MyToolbar', cls=MyToolbar)
        self.screen_manager = Builder.load_string(KV)
        # Флаг, указывающий, что упражнение выполняется
        self.exercise_running = False
        return self.screen_manager

    def log_diary(self, entry):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {entry}"
        self.diary_entries.append(log_entry)
        # Сохраняем запись в файл (добавляем в конец)
        with open(self.diary_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
        print(log_entry)

    def get_diary_entries(self):
        if self.diary_entries:
            return "\n".join(self.diary_entries)
        else:
            return "Дневник пуст"

    def start_technique(self, technique):
        # Логирование выбранной техники
        self.log_diary(f"Выбрана техника: {technique}")
        self.exercise_running = True  # устанавливаем флаг, что упражнение запущено
        
        # Запускаем таймер на 90 секунд
        Clock.schedule_once(self.stop_exercise, 90)
        
        # Конфигурация для каждой техники
        configs = {
            "Квадратное дыхание": {"min_size": 50, "max_size": 200, "expand_duration": 2, "contract_duration": 2},
            "Дыхание Нади Шодхана": {"min_size": 50, "max_size": 180, "expand_duration": 2.5, "contract_duration": 2.5},
            "Диафрагмальное дыхание": {"min_size": 60, "max_size": 210, "expand_duration": 3, "contract_duration": 3},
            "Дыхание 4-7-8": {"min_size": 50, "max_size": 220, "expand_duration": 4, "contract_duration": 7},
        }
        config = configs.get(technique, {"min_size": 50, "max_size": 200, "expand_duration": 2, "contract_duration": 2})
        
        # Находим слой для анимации, который находится поверх UI
        main_screen = self.root.get_screen('main')
        animation_layer = main_screen.ids.animation_layer
        animation_layer.clear_widgets()
        
        # Создаем виджет шара и устанавливаем его начальный размер
        circle = CircleWidget()
        circle.circle_size = config["min_size"]
        animation_layer.add_widget(circle)
        
        # Добавляем надпись для вдоха/выдоха, располагаем выше шара
        breathing_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Primary",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_style="H4"
        )
        animation_layer.add_widget(breathing_label)
        
        # Определяем цикл дыхания с анимацией
        def breathing_cycle(*args):
            if not self.exercise_running:
                return
            breathing_label.text = "Вдох"
            anim_expand = Animation(circle_size=config["max_size"], duration=config["expand_duration"])
    
            def on_expand_complete(animation, widget):
                if not self.exercise_running:
                    return
                breathing_label.text = "Выдох"
                anim_contract = Animation(circle_size=config["min_size"], duration=config["contract_duration"])
                anim_contract.bind(on_complete=lambda a, w: breathing_cycle())
                anim_contract.start(circle)
    
            anim_expand.bind(on_complete=on_expand_complete)
            anim_expand.start(circle)
        
        breathing_cycle()

    def stop_exercise(self, *args):
        # Останавливаем упражнение, сбрасывая флаг и очищая слой анимации
        self.exercise_running = False
        main_screen = self.root.get_screen('main')
        animation_layer = main_screen.ids.animation_layer
        animation_layer.clear_widgets()
        self.log_diary("Упражнение завершено (90 секунд)")
        # Переходим на экран конечного опроса через 1 секунду
        Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'endsurvey'), 1)

if __name__ == '__main__':
    BreathingApp().run()
