from app import *
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%                                                                                              %
#%                                                                                              %
#%                                          ПРИЛОЖЕНИЕ                                          %
#%                                                                                              %
#%                                                                                              %
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



class MyApp(App):
    title = 'iTarget'

    def build(self):
        screen_manager = ScreenManager()

        home_screen = HomeScreen(name='home')
        training_settings_screen = TrainingsSettingsScreen(name='tr_st')
        stats_screen = StatsScreen(name='stats')
        training_screen= TrainingScreen(name= 'tr')

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(training_settings_screen)
        screen_manager.add_widget(stats_screen)
        screen_manager.add_widget(training_screen)



        full_layout = BoxLayout(orientation='vertical')
        with full_layout.canvas:
            Color(0,225,12, 0.5)
            Rectangle(size= (1000,1000))
        full_layout.add_widget(screen_manager)

        layout_buttons = GridLayout(cols=2, spacing=-2.5, size_hint_y=0.1)

        def on_button_release1(self):
            screen_manager.current = 'home'
        button_home = Button(text="Trainings", size_hint_x=10, background_color= (0,0,0,0.35))
        button_home.bind(on_press=on_button_release1)

        def on_button_release2(self):
            screen_manager.current = 'stats'
        button_stats = Button(text='Stats', size_hint_x=10, background_color= (0,0,0,0.35))
        button_stats.bind(on_press=on_button_release2)

        layout_buttons.add_widget(button_home)
        layout_buttons.add_widget(button_stats)

        full_layout.add_widget(layout_buttons)

        screen_manager.current = 'home'  # Начальный экран

        return full_layout


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __name__ == "__main__":
    MyApp().run()