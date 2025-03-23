import customtkinter as ctk
import tkinter as tk
from tkinter.filedialog import askopenfilename

import pandas as pd
import geopandas as gpd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import colormaps as mpl_color_maps
from matplotlib.figure import Figure

from os import listdir
import chardet

import db_connection

from pandastable import Table

ctk.set_appearance_mode('dark')


def read_and_transform_data_for_example_chart(output_data_year: str) -> pd.DataFrame:
    airports_charter_by_metropolis_frame = pd.read_csv(
        'C:/Users/adria/PycharmProjects/Kwintesencjozator_ambarasu_3000/.venv/data/data_sets/wg_metropolii_czarter_4kw2023.csv')
    airports_charter_by_metropolis_frame = airports_charter_by_metropolis_frame.drop(
        ['nazwa_zmiennej', 'typ_ruchu_lotniczego', 'przedzial_czasu'], axis=1)
    airports_charter_by_metropolis_frame = airports_charter_by_metropolis_frame.set_index('miasto')
    airports_charter_by_metropolis_frame_2022 = airports_charter_by_metropolis_frame.loc[
        airports_charter_by_metropolis_frame['rok'] == 2022]
    airports_charter_by_metropolis_frame_2023 = airports_charter_by_metropolis_frame.loc[
        airports_charter_by_metropolis_frame['rok'] == 2023]

    match output_data_year:
        case '2022':
            return airports_charter_by_metropolis_frame_2022
        case '2023':
            return airports_charter_by_metropolis_frame_2023
        case _:
            raise ValueError(
                f"Invalid value passed as an attribute for {read_and_transform_data_for_example_chart.__name__}")


class ApplicationScreenRoot(ctk.CTk):
    def __init__(self, db_object: db_connection.Db):
        super().__init__()
        self.data_frame = pd.DataFrame()
        self.title("GeoDataAnalytics")
        self.geometry("800x800")
        self.iconbitmap('C:/Users/adria/PycharmProjects/GeoAnalitycsDesktopApp/.venv/data/images/icon.ico')
        self.db_object = db_object
        self.basic_font_props = ("Helvetica", 15)
        self.smaller_font_props = ("Helvetica", 12)
        self.bigger_font_props = ("Helvetica", 24)

        self.color_bank = pd.DataFrame({'dark': dict(background_color="#121413",
                                                     widget_color="#4EC169",
                                                     hover_color="#537761",
                                                     border_color="#707972",
                                                     text_color="#EBF7EF",
                                                     darker_widget_color='#338A48'),
                                        'light': dict(background_color="#a0a3a2",
                                                      widget_color="#79e659",
                                                      hover_color="#417B30",
                                                      border_color="#424E3E",
                                                      text_color="#020202",
                                                      darker_widget_color='#3C6F2D')}
                                       )

        self.login_frame = ctk.CTkFrame(self,
                                        width=700,
                                        height=500,
                                        fg_color=self.color_bank['dark'].loc['background_color'],
                                        corner_radius=7
                                        )

        self.plot_frame = ctk.CTkFrame(self,
                                       height=400,
                                       width=1400,
                                       fg_color=self.color_bank['dark'].loc['background_color'],
                                       corner_radius=0
                                       )

        self.chart_choice_frame = ctk.CTkFrame(self,
                                               height=150,
                                               fg_color=self.color_bank['dark'].loc['background_color'],
                                               border_width=0,
                                               corner_radius=0
                                               )

        self.frame_including_datasets_scrollable_frame_and_back_to_login_button = ctk.CTkFrame(self,
                                                                                               width=800,
                                                                                               height=800,
                                                                                               corner_radius=10,
                                                                                               fg_color=self.color_bank[
                                                                                                   'dark'].loc[
                                                                                                   'background_color']
                                                                                               )
        self.first_dataset_to_connect__frame = ctk.CTkFrame(self,
                                                            width=1600,
                                                            height=500,
                                                            corner_radius=10,
                                                            fg_color=self.color_bank['dark'].loc['background_color']
                                                            )

        self.second_dataset_to_connect__frame = ctk.CTkFrame(self,
                                                             width=1600,
                                                             height=500,
                                                             corner_radius=10,
                                                             fg_color=self.color_bank['dark'].loc['background_color']
                                                             )

        self.shp_file_processing_main_frame = ctk.CTkFrame(self,
                                                           width=1600,
                                                           height=500,
                                                           corner_radius=10,
                                                           fg_color=self.color_bank['dark'].loc['background_color']
                                                           )
        self.shp_file_processing_main_frame.columnconfigure(index=(0, 1, 2, 3, 4, 5), weight=1)
        self.shp_file_processing_main_frame.rowconfigure(index=(0, 1, 2), weight=1)

        self.shp_file_processing_additional_frame = ctk.CTkFrame(self,
                                                                 width=1600,
                                                                 height=500,
                                                                 corner_radius=10,
                                                                 fg_color=self.color_bank['dark'].loc[
                                                                     'background_color']
                                                                 )

        class LoginFrameUtilities:
            def __init__(self, root_object, db_object: db_connection.Db, login_frame_object: ctk.CTkFrame):
                self.login_process_execution_label = ctk.CTkLabel(login_frame_object,
                                                                  text="",
                                                                  font=root_object.bigger_font_props,
                                                                  text_color=root_object.color_bank['dark'].loc[
                                                                      'text_color']
                                                                  )

                self.login_entry = ctk.CTkEntry(login_frame_object,
                                                placeholder_text="Enter your login (e-mail address)",
                                                placeholder_text_color=root_object.color_bank['dark'].loc['text_color'],
                                                text_color=root_object.color_bank['dark'].loc['text_color'],
                                                width=250,
                                                height=40,
                                                )

                self.password_entry = ctk.CTkEntry(login_frame_object,
                                                   placeholder_text="Enter your password",
                                                   placeholder_text_color=root_object.color_bank['dark'].loc[
                                                       'text_color'],
                                                   text_color=root_object.color_bank['dark'].loc['text_color'],
                                                   width=250,
                                                   height=40,
                                                   show="*"
                                                   )
                self.login_process_entries = [self.password_entry, self.login_entry]
                self.remember_me_checkbox_variable = ctk.BooleanVar()
                self.remember_me_checkbox = ctk.CTkCheckBox(login_frame_object,
                                                            text="Remember me",
                                                            height=35,
                                                            width=100,
                                                            font=root_object.basic_font_props,
                                                            text_color=root_object.color_bank['dark'].loc['text_color'],
                                                            fg_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            hover_color=root_object.color_bank['dark'].loc[
                                                                'hover_color'],
                                                            corner_radius=10,
                                                            border_width=3,
                                                            border_color=root_object.color_bank['dark'].loc[
                                                                'border_color'],
                                                            variable=self.remember_me_checkbox_variable,
                                                            )

                self.submit_button = ctk.CTkButton(login_frame_object,
                                                   text="Submit",
                                                   command=lambda: db_object._login_processing(root_object),
                                                   height=35,
                                                   width=110,
                                                   font=root_object.basic_font_props,
                                                   text_color=root_object.color_bank['dark'].loc['text_color'],
                                                   fg_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                                                   hover_color=root_object.color_bank['dark'].loc['hover_color'],
                                                   border_color=root_object.color_bank['dark'].loc['border_color'],
                                                   corner_radius=10,
                                                   border_width=3
                                                   )

                self.enter_as_guest_button = ctk.CTkButton(login_frame_object,
                                                           text="Enter as guest (limited access)",
                                                           command=lambda: root_object.example_plot_and_chart_choice_frame_utilities.guest_login_processing(
                                                               root_object),
                                                           height=35,
                                                           width=250,
                                                           font=root_object.basic_font_props,
                                                           text_color=root_object.color_bank['dark'].loc['text_color'],
                                                           fg_color=root_object.color_bank['dark'].loc[
                                                               'darker_widget_color'],
                                                           hover_color=root_object.color_bank['dark'].loc[
                                                               'hover_color'],
                                                           border_color=root_object.color_bank['dark'].loc[
                                                               'border_color'],
                                                           corner_radius=10,
                                                           border_width=3
                                                           )

                fullscreen_switch_value = ctk.StringVar(value="windowed")
                self.fullscreen_switch = ctk.CTkSwitch(login_frame_object,
                                                       text="Fullscreen 🢄🢆",
                                                       height=12,
                                                       width=50,
                                                       font=root_object.smaller_font_props,
                                                       text_color=root_object.color_bank['dark'].loc['text_color'],
                                                       fg_color=root_object.color_bank['dark'].loc[
                                                           'darker_widget_color'],
                                                       border_color=root_object.color_bank['dark'].loc['border_color'],
                                                       corner_radius=10,
                                                       border_width=4,
                                                       command=lambda: self.fullscreen_switch_operation(
                                                           fullscreen_switch_value=fullscreen_switch_value,
                                                           root_object=root_object),
                                                       variable=fullscreen_switch_value,
                                                       onvalue='fullscreen',
                                                       offvalue='windowed'
                                                       )

                self.color_value = ctk.StringVar()
                self.appearance_color_switch = ctk.CTkSwitch(login_frame_object,
                                                             text="Light mode ☾ 🡪 ☀",
                                                             height=12,
                                                             width=50,
                                                             font=root_object.smaller_font_props,
                                                             text_color=root_object.color_bank['dark'].loc[
                                                                 'text_color'],
                                                             fg_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             corner_radius=10,
                                                             border_width=3,
                                                             border_color=root_object.color_bank['dark'].loc[
                                                                 'border_color'],
                                                             command=lambda: self.switch_appearance_mode(
                                                                 color_theme=self.color_value, root_object=root_object),
                                                             variable=self.color_value,
                                                             onvalue='light',
                                                             offvalue='dark'
                                                             )

            def pack_widgets(self) -> None:
                self.login_process_execution_label.pack(pady=35)
                self.login_entry.pack(pady=5)
                self.password_entry.pack(pady=5)
                self.remember_me_checkbox.pack(pady=5)
                self.submit_button.pack(pady=5)
                self.enter_as_guest_button.pack(pady=5)
                self.fullscreen_switch.pack(pady=20)
                self.appearance_color_switch.pack(pady=5)


            def switch_all_widgets_color(self, mode: str, root_object) -> None:
                for widget in root_object.all_widgets:
                    if hasattr(widget, 'configure'):
                        match type(widget):
                            case ctk.CTkEntry:
                                widget.configure(
                                    placeholder_text_color=root_object.color_bank[mode].loc['text_color'],
                                    fg_color=root_object.color_bank[mode].loc['darker_widget_color'],
                                    text_color=root_object.color_bank[mode].loc['text_color'],
                                    border_color=root_object.color_bank[mode].loc['border_color']
                                )

                            case ctk.CTkSwitch:
                                widget.configure(
                                    fg_color=root_object.color_bank[mode].loc['darker_widget_color'],
                                    text_color=root_object.color_bank[mode].loc['text_color'],
                                    border_color=root_object.color_bank[mode].loc['border_color']
                                )

                            case ctk.CTkLabel:
                                widget.configure(
                                    text_color=root_object.color_bank[mode].loc['text_color']
                                )
                            case _:
                                widget.configure(
                                    fg_color=root_object.color_bank[mode].loc['darker_widget_color'],
                                    text_color=root_object.color_bank[mode].loc['text_color'],
                                    border_color=root_object.color_bank[mode].loc['border_color']
                                )

            def switch_all_frames_color(self, mode: str, root_object) -> None:
                for frame in root_object.all_frames:
                    frame.configure(
                        fg_color=root_object.color_bank[mode].loc['background_color']
                    )

            def switch_appearance_mode(self, color_theme: ctk.StringVar, root_object) -> None:
                theme_string_value = color_theme.get()
                match theme_string_value:
                    case "dark":
                        ctk.set_appearance_mode(theme_string_value)
                        self.appearance_color_switch.configure(text='Light mode ☾ 🡪 ☀')
                        self.switch_all_widgets_color(theme_string_value, root_object)
                        self.switch_all_frames_color(theme_string_value, root_object)
                    case "light":
                        ctk.set_appearance_mode(theme_string_value)
                        self.appearance_color_switch.configure(text='Dark mode ☀ 🡪 ☾')
                        self.switch_all_widgets_color(theme_string_value, root_object)
                        self.switch_all_frames_color(theme_string_value, root_object)
                    case _:
                        raise f'Unable to switch to {theme_string_value} mode.'

            def fullscreen_switch_operation(self,
                                            fullscreen_switch_value: ctk.StringVar,
                                            root_object
                                            ) -> None:
                fullscreen_switch_value = fullscreen_switch_value.get()

                match fullscreen_switch_value:
                    case "fullscreen":
                        root_object.state('zoomed')
                        self.fullscreen_switch.configure(text='Windowed 🢆🢄')
                    case "windowed":
                        root_object.geometry('700x500')
                        root_object.state('normal')
                        self.fullscreen_switch.configure(text='Fullscreen 🢄🢆')
                    case _:
                        raise ValueError(f'Unknown switch value {fullscreen_switch_value}')

        class ExamplePlotAndChartChoiceFrameUtilities:
            def __init__(self, root_object):
                example_chart_years_list = ['2022', '2023']

                self.back_to_login_screen_button = ctk.CTkButton(root_object.chart_choice_frame,
                                                                 text="Go back to login screen",
                                                                 command=lambda: self.get_back_to_login_screen(
                                                                     root_object),
                                                                 height=25,
                                                                 width=100,
                                                                 font=root_object.basic_font_props,
                                                                 text_color=root_object.color_bank['dark'].loc[
                                                                     'text_color'],
                                                                 fg_color=root_object.color_bank['dark'].loc[
                                                                     'darker_widget_color'],
                                                                 hover_color=root_object.color_bank['dark'].loc[
                                                                     'hover_color'],
                                                                 border_color=root_object.color_bank['dark'].loc[
                                                                     'border_color'],
                                                                 corner_radius=10,
                                                                 border_width=3
                                                                 )

                self.which_year_label = ctk.CTkLabel(root_object.chart_choice_frame,
                                                     text="Year of displayed data: ",
                                                     font=root_object.bigger_font_props,
                                                     text_color=root_object.color_bank['dark'].loc['text_color']
                                                     )

                self.which_year_combo_box = ctk.CTkComboBox(root_object.chart_choice_frame,
                                                            width=80,
                                                            height=40,
                                                            fg_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            button_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            corner_radius=0,
                                                            values=example_chart_years_list,
                                                            command=lambda get_value: self.plot_example_chart(
                                                                root_object, get_value)
                                                            )

            def plot_example_chart(self, root_object, year_chosen_from_combo_box: str) -> None:
                root_object.is_figure_defined_if_no_then_define_it_and_create_canvas_widget(self, "plot_frame",
                                                                                            root_object)

                example_chart_data_frame = read_and_transform_data_for_example_chart(year_chosen_from_combo_box).head()

                example_chart_data_frame.plot(
                    ax=self.ax, y='liczba_pasazerow', ylabel="",
                    kind='pie',
                    fontsize=root_object.basic_font_props[1], autopct='%.0f%%',
                    textprops={'color': 'w'},
                    labels=[''] * 5,
                    explode=[0.1] * 5,
                    wedgeprops={'edgecolor': 'black'},
                    shadow=True,
                    legend=True,
                    pctdistance=0.6
                )
                self.ax.set_title(
                    f"Example pie chart\n"
                    f"(Top 5 flight destinations from Polish airports in {year_chosen_from_combo_box})",
                    color='white', fontweight='bold', fontsize=root_object.bigger_font_props[1],
                    y=0.92
                )
                self.ax.legend(labels=example_chart_data_frame.index,
                               bbox_to_anchor=(1, -0.15, 0.5, 1)
                               )

                self.canvas.draw()

            def get_back_to_login_screen(self, root_object) -> None:
                root_object.pack_forget_visible_elements([root_object.chart_choice_frame, root_object.plot_frame])
                root_object.login_frame.pack_propagate(False)
                root_object.login_frame.pack(pady=10, anchor='center')

            def guest_login_processing(self, root_object) -> None:
                self.back_to_login_screen_button.pack(pady=20)
                root_object.login_frame.pack_forget()
                self.position_widgets_inside_chart_frame(root_object=root_object)
                root_object.plot_frame.pack(fill='x')

            def position_widgets_inside_chart_frame(self, root_object) -> None:
                root_object.chart_choice_frame.pack(fill='x')
                self.which_year_label.pack(pady=10)
                self.which_year_combo_box.pack(pady=10)

        self.example_plot_and_chart_choice_frame_utilities = ExamplePlotAndChartChoiceFrameUtilities(root_object=self)
        self.login_frame_utilities = LoginFrameUtilities(self, db_object, self.login_frame)

        class FrameIncludingDatasetsScrollableFrameAndBackToLoginButtonUtilities:
            def __init__(self, root_object):
                self.dictionary_of_datasets_buttons = {}
                self.plot_parameters = {}

                self.import_users_data_button = ctk.CTkButton(
                    root_object.frame_including_datasets_scrollable_frame_and_back_to_login_button,
                    text="Import users data (any excel type)",
                    height=35,
                    width=100,
                    font=root_object.bigger_font_props,
                    text_color=root_object.color_bank['dark'].loc['text_color'],
                    fg_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                    hover_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                    corner_radius=10,
                    border_width=5,
                    border_color=root_object.color_bank['dark'].loc['border_color'],
                    command=lambda: self.go_to_import_users_data_screen(root_object=root_object)
                )

                self.datasets_scrollable_frame = ctk.CTkScrollableFrame(
                    root_object.frame_including_datasets_scrollable_frame_and_back_to_login_button,
                    width=700,
                    height=500,
                    label_font=root_object.bigger_font_props,
                    label_text="\nChoose dataset from the following\n",
                    label_text_color=root_object.color_bank['dark'].loc['text_color'],
                    label_fg_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                    corner_radius=5,
                    fg_color=root_object.color_bank['dark'].loc['background_color']
                )

                self.back_to_login_screen_from_datasets_choosing_button = ctk.CTkButton(
                    root_object.frame_including_datasets_scrollable_frame_and_back_to_login_button,
                    text="Back to login screen",
                    height=35,
                    width=100,
                    font=root_object.bigger_font_props,
                    text_color=root_object.color_bank['dark'].loc['text_color'],
                    fg_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                    hover_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                    corner_radius=10,
                    border_width=5,
                    border_color=root_object.color_bank['dark'].loc['border_color'],
                    command=lambda: self.back_to_login_screen_from_datasets_choosing(root_object)
                )

                colors_list = ["red", "green", "blue", "black", "white", "orange"]
                self.color_combo_box_in_shp_frame = ctk.CTkComboBox(root_object.shp_file_processing_main_frame,
                                                                    state="readonly",
                                                                    width=160,
                                                                    height=40,
                                                                    fg_color=root_object.color_bank['dark'].loc[
                                                                        'darker_widget_color'],
                                                                    button_color=root_object.color_bank['dark'].loc[
                                                                        'darker_widget_color'],
                                                                    corner_radius=0,
                                                                    values=colors_list,
                                                                    command=lambda
                                                                        new_color_value: self.set_color_value(
                                                                        new_color_value)
                                                                    )

                color_maps_list = list(mpl_color_maps)[:20]
                self.color_maps_combo_box_in_shp_frame = ctk.CTkComboBox(root_object.shp_file_processing_main_frame,
                                                                         state="readonly",
                                                                         width=160,
                                                                         height=40,
                                                                         fg_color=root_object.color_bank['dark'].loc[
                                                                             'darker_widget_color'],
                                                                         button_color=
                                                                         root_object.color_bank['dark'].loc[
                                                                             'darker_widget_color'],
                                                                         corner_radius=0,
                                                                         values=color_maps_list,
                                                                         command=lambda
                                                                             new_color_map_value: self.set_color_map_value(
                                                                             new_color_map_value)
                                                                         )

                self.column_base_for_color_map_combo_box_in_shp_frame = ctk.CTkComboBox(
                    root_object.shp_file_processing_main_frame,
                    state="readonly",
                    width=220,
                    height=40,
                    fg_color=root_object.color_bank['dark'].loc[
                        'darker_widget_color'],
                    button_color=
                    root_object.color_bank['dark'].loc[
                        'darker_widget_color'],
                    corner_radius=0,
                    command=lambda
                        new_column_base_value: self.set_column_base_for_cmap(
                        new_column_base_value)
                )

                self.edge_color_combo_box_in_shp_frame = ctk.CTkComboBox(root_object.shp_file_processing_main_frame,
                                                                         state="readonly",
                                                                         width=220,
                                                                         height=40,
                                                                         fg_color=root_object.color_bank['dark'].loc[
                                                                             'darker_widget_color'],
                                                                         button_color=
                                                                         root_object.color_bank['dark'].loc[
                                                                             'darker_widget_color'],
                                                                         corner_radius=0,
                                                                         values=colors_list,
                                                                         command=lambda
                                                                             new_color_value: self.set_edge_color_value(
                                                                             new_color_value)
                                                                         )

                self.submit_all_parameters_and_visualize_button = ctk.CTkButton(
                    root_object.shp_file_processing_main_frame,
                    text="Submit all parameters \nand visualize",
                    height=40,
                    width=160,
                    font=root_object.smaller_font_props,
                    text_color=root_object.color_bank['dark'].loc['text_color'],
                    fg_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                    hover_color=root_object.color_bank['dark'].loc['hover_color'],
                    corner_radius=0,
                    border_width=3,
                    border_color=root_object.color_bank['dark'].loc['border_color'],
                    command=lambda: self.submit_all_parameters_and_visualize_geospatial_action(root_object=root_object)
                )

            def set_column_base_for_cmap(self, new_column_base):
                self.plot_parameters['column'] = new_column_base

            def set_color_map_value(self, new_color_map_value):
                self.plot_parameters['cmap'] = new_color_map_value
                if "column" not in self.plot_parameters.keys():
                    self.plot_parameters['column'] = self.data_frame_columns[0]

            def set_color_value(self, new_object_color_value):
                self.plot_parameters['color'] = new_object_color_value

            def set_edge_color_value(self, new_edge_color_value):
                self.plot_parameters['edgecolor'] = new_edge_color_value

            def submit_all_parameters_and_visualize_geospatial_action(self, root_object):
                root_object.is_figure_defined_if_no_then_define_it_and_create_canvas_widget(
                    self,
                    "shp_file_processing_additional_frame",
                    root_object
                )
                match not self.plot_parameters:
                    case True:
                        root_object.data_frame.content.plot(ax=self.ax)
                    case False:
                        root_object.data_frame.content.plot(
                            ax=self.ax,
                            **self.plot_parameters
                        )

                self.canvas.draw()
                self.plot_parameters = {}
                self.reset_comboboxes()

            def reset_comboboxes(self):
                self.edge_color_combo_box_in_shp_frame.set("Color of edges:")
                self.color_combo_box_in_shp_frame.set("Color of elements:")
                self.column_base_for_color_map_combo_box_in_shp_frame.set("Base (column)\nfor color map:")
                self.color_maps_combo_box_in_shp_frame.set("Color maps:")

            def go_to_import_users_data_screen(self, root_object):
                root_object.pack_forget_visible_elements(
                    root_object.frame_including_datasets_scrollable_frame_and_back_to_login_button)
                root_object.import_users_data_frame.pack(pady=10)
                root_object.confirm_data_importing_process_button.pack(pady=20)
                root_object.import_xlsx_file_path = askopenfilename(title="Select excel file",
                                                                    filetypes=(("xlsx file", "*.xlsx"),
                                                                               ("xls file", "*.xls")))


            def back_to_login_screen_from_datasets_choosing(self, root_object):
                root_object.pack_forget_visible_elements(
                    root_object.frame_including_datasets_scrollable_frame_and_back_to_login_button)
                root_object.pack_login_frame()
                root_object.login_frame_utilities.pack_widgets()
                root_object.login_frame_utilities.login_entry.configure(placeholder_text="Enter your e-mail")
                root_object.login_frame_utilities.password_entry.configure(placeholder_text="Enter your password")

            def pack_datasets_buttons_on_scrollable_frame(self) -> None:
                for button in self.dictionary_of_datasets_buttons.values():
                    button.pack(pady=10)

            def create_buttons_of_datasets(self, datasets_names: dict[str, str], root_object) -> None:
                for dataset_name_with_extension in datasets_names.keys():
                    dataset_name_without_extension = dataset_name_with_extension.rsplit(sep='.')[0]
                    dataset_button = ctk.CTkButton(self.datasets_scrollable_frame,
                                                   text_color=root_object.color_bank['dark'].loc['text_color'],
                                                   fg_color=root_object.color_bank['dark'].loc['darker_widget_color'],
                                                   hover_color=root_object.color_bank['dark'].loc['background_color'],
                                                   font=root_object.smaller_font_props,
                                                   text=dataset_name_without_extension,
                                                   height=40,
                                                   width=self.datasets_scrollable_frame.cget('width') - 250,
                                                   corner_radius=0,
                                                   )

                    try:
                        root_object.all_widgets.append(dataset_button)
                    except AttributeError:
                        root_object.all_widgets = []
                        root_object.all_widgets.append(dataset_button)

                    self.dictionary_of_datasets_buttons[dataset_name_with_extension] = dataset_button

            def dataset_button_operation(self, dataset_name: str, root_object) -> None:
                file_extension = datasets.dictionary_of_dataset_name_and_its_path[dataset_name].rsplit(sep=".")[-1]
                dataset_path = datasets.dictionary_of_dataset_name_and_its_path[dataset_name]
                match file_extension:
                    case "csv":
                        try:
                            root_object.csv_processing_screen(
                                file_path=dataset_path
                            )
                        except FileNotFoundError:
                            print(f"File not found path: {dataset_path}")

                    case "xlsx":
                        root_object.data_frame.content = pd.read_excel(
                            io=dataset_path
                        )
                        root_object.xlsx_processing_screen(file_path=dataset_path)
                    case "txt":
                        root_object.csv_processing_screen(
                            file_path=dataset_path
                        )
                    case "json":
                        root_object.data_frame.content = pd.read_json(
                            path_or_buf=dataset_path
                        )
                        root_object.json_processing_screen(file_path=dataset_path)
                    case "shp":
                        root_object.data_frame.content = gpd.read_file(
                            dataset_path
                        )
                        self.shp_file_frame_visualization(root_object)

            def shp_file_frame_visualization(self, root_object):
                self.data_frame_columns = [column_name
                                           for column_name in root_object.data_frame.content.columns
                                           if column_name != "geometry"
                                           ]
                root_object.pack_forget_visible_elements(
                    root_object.frame_including_datasets_scrollable_frame_and_back_to_login_button)
                root_object.shp_file_processing_main_frame.pack(pady=10)
                root_object.shp_file_processing_additional_frame.pack(pady=10)
                self.reset_comboboxes()
                self.color_combo_box_in_shp_frame.grid(row=0, column=0)
                self.edge_color_combo_box_in_shp_frame.grid(row=0, column=1)
                self.color_maps_combo_box_in_shp_frame.grid(row=1, column=0)
                self.submit_all_parameters_and_visualize_button.grid(row=2, column=0)
                self.column_base_for_color_map_combo_box_in_shp_frame.configure(values=self.data_frame_columns)
                self.column_base_for_color_map_combo_box_in_shp_frame.grid(row=1, column=1)

            def set_command_for_datasets_buttons(self, root_object) -> None:
                for button_name, button_object in self.dictionary_of_datasets_buttons.items():
                    button_object.configure(
                        command=lambda dataset_name=button_name: self.dataset_button_operation(
                            dataset_name=dataset_name, root_object=root_object))

        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities = FrameIncludingDatasetsScrollableFrameAndBackToLoginButtonUtilities(
            root_object=self)

        class GridFrameContainingCsvOptionsUtilities:
            def __init__(self, root_object):
                self.visualization_type = None
                self.selected_columns_checkboxes_to_usecols = {}
                self.data_frames_list = []
                self.dictionary_of_read_csv_arguments = {}
                self.dictionary_of_columns_to_become_index_checkboxes = {}
                self.dictionary_of_columns_checkboxes = {}
                self.low_memory_argument = ctk.IntVar(value=1)
                separators_list = [".", ";", 'tabulator', 'new line sign']
                quote_chars_list = ["' '", '" "']
                chart_types_list = ["bar", "stairs", "scatter", "stem", "pie", "hist", "box", "hexbin"]

                self.geospatial_visualization_button = ctk.CTkButton(root_object,
                                                                     font=root_object.smaller_font_props,
                                                                     corner_radius=0,
                                                                     text_color=root_object.color_bank['dark'].loc[
                                                                         'text_color'],
                                                                     fg_color=root_object.color_bank['dark'].loc[
                                                                         'darker_widget_color'],
                                                                     hover_color=root_object.color_bank['dark'].loc[
                                                                         'darker_widget_color'],
                                                                     border_color=root_object.color_bank['dark'].loc[
                                                                         'border_color'],
                                                                     text='Submit x and y parameters and go to geospatial visualization menu',
                                                                     command=lambda: self.replace_classic_visualization_with_geospatial_visualization(
                                                                         root_object=root_object)
                                                                     )

                self.chart_types_combo_box = ctk.CTkComboBox(root_object,
                                                             state="readonly",
                                                             font=root_object.smaller_font_props,
                                                             fg_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             button_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             corner_radius=0,
                                                             border_width=0,
                                                             values=chart_types_list,
                                                             command=lambda chart_type: self.set_chart_type(chart_type,
                                                                                                            root_object)
                                                             )

                self.data_table_frame = ctk.CTkFrame(root_object,
                                                     height=400,
                                                     width=1200,
                                                     fg_color=root_object.color_bank['dark'].loc['background_color'],
                                                     corner_radius=0
                                                     )
                self.optionally_select_columns_button = ctk.CTkButton(root_object.grid_frame,
                                                                      font=root_object.smaller_font_props,
                                                                      corner_radius=0,
                                                                      text_color=root_object.color_bank['dark'].loc[
                                                                          'text_color'],
                                                                      fg_color=root_object.color_bank['dark'].loc[
                                                                          'darker_widget_color'],
                                                                      hover_color=root_object.color_bank['dark'].loc[
                                                                          'darker_widget_color'],
                                                                      border_color=root_object.color_bank['dark'].loc[
                                                                          'border_color'],
                                                                      text='Select columns to import\n'
                                                                           '(Default - all columns)',
                                                                      command=self.replace_select_columns_button_with_columns_choose_frame
                                                                      )

                self.columns_to_choose_to_become_usecols_scroll_frame = ctk.CTkScrollableFrame(root_object.grid_frame,
                                                                                               label_font=root_object.smaller_font_props,
                                                                                               label_text="Columns:",
                                                                                               label_text_color=
                                                                                               root_object.color_bank[
                                                                                                   'dark'].loc[
                                                                                                   'text_color'],
                                                                                               label_fg_color=
                                                                                               root_object.color_bank[
                                                                                                   'dark'].loc[
                                                                                                   'darker_widget_color'
                                                                                               ],
                                                                                               corner_radius=0,
                                                                                               bg_color=
                                                                                               root_object.color_bank[
                                                                                                   'dark'].loc[
                                                                                                   'background_color']
                                                                                               )

                self.columns_to_choose_to_become_index_scroll_frame = ctk.CTkScrollableFrame(root_object.grid_frame,
                                                                                             label_font=root_object.smaller_font_props,
                                                                                             label_text="Index column('s):",
                                                                                             label_text_color=
                                                                                             root_object.color_bank[
                                                                                                 'dark'].loc[
                                                                                                 'text_color'],
                                                                                             label_fg_color=
                                                                                             root_object.color_bank[
                                                                                                 'dark'].loc[
                                                                                                 'darker_widget_color'],
                                                                                             corner_radius=0,
                                                                                             bg_color=
                                                                                             root_object.color_bank[
                                                                                                 'dark'].loc[
                                                                                                 'background_color']
                                                                                             )

                self.submit_columns_to_become_in_usecols_argument_button = ctk.CTkButton(root_object.grid_frame,
                                                                                         text="Submit chosen columns",
                                                                                         height=30,
                                                                                         width=100,
                                                                                         font=root_object.smaller_font_props,
                                                                                         text_color=
                                                                                         root_object.color_bank[
                                                                                             'dark'].loc['text_color'],
                                                                                         fg_color=
                                                                                         root_object.color_bank[
                                                                                             'dark'].loc[
                                                                                             'darker_widget_color'],
                                                                                         hover_color=
                                                                                         root_object.color_bank[
                                                                                             'dark'].loc['hover_color'],
                                                                                         corner_radius=0,
                                                                                         border_width=3,
                                                                                         border_color=
                                                                                         root_object.color_bank[
                                                                                             'dark'].loc[
                                                                                             'border_color'],
                                                                                         command=lambda: self.submit_columns_to_become_in_usecols_argument_action(
                                                                                             root_object)
                                                                                         )

                self.quote_char_combobox = ctk.CTkComboBox(root_object.grid_frame,
                                                           state="readonly",
                                                           font=root_object.smaller_font_props,
                                                           fg_color=root_object.color_bank['dark'].loc[
                                                               'darker_widget_color'],
                                                           button_color=root_object.color_bank['dark'].loc[
                                                               'darker_widget_color'],
                                                           corner_radius=0,
                                                           border_width=0,
                                                           values=quote_chars_list,
                                                           command=lambda
                                                               combobox_char_value: self.action_after_choosing_quote_char(
                                                               quote_char_chosen_from_combobox=combobox_char_value,
                                                               data_frame_properties=root_object.data_frame)
                                                           )

                self.separators_combo_box = ctk.CTkComboBox(root_object.grid_frame,
                                                            state="readonly",
                                                            font=root_object.smaller_font_props,
                                                            fg_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            button_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            corner_radius=0,
                                                            border_width=0,
                                                            values=separators_list,
                                                            command=lambda
                                                                combobox_value: self.action_after_choosing_separator(
                                                                separator_chosen_from_combobox=combobox_value,
                                                                data_frame_properties=root_object.data_frame)
                                                            )

                self.low_memory_switch = ctk.CTkSwitch(root_object.grid_frame,
                                                       text="Low memory\nTrue",
                                                       font=root_object.smaller_font_props,
                                                       text_color=root_object.color_bank['dark'].loc[
                                                           'text_color'],
                                                       fg_color=root_object.color_bank['dark'].loc[
                                                           'darker_widget_color'],
                                                       bg_color='transparent',
                                                       progress_color=root_object.color_bank['dark'].loc[
                                                           'hover_color'],
                                                       corner_radius=10,
                                                       border_width=3,
                                                       border_color=root_object.color_bank['dark'].loc[
                                                           'border_color'],
                                                       variable=self.low_memory_argument,
                                                       onvalue=0,
                                                       offvalue=1,
                                                       command=lambda: self.low_memory_switch.configure(
                                                           text=f"Low memory\n{'True' if self.low_memory_argument.get() == 1 else 'False'}"),
                                                       )

                self.submit_everything_button = ctk.CTkButton(root_object.grid_frame,
                                                              text="Submit everything",
                                                              height=30,
                                                              width=100,
                                                              font=root_object.smaller_font_props,
                                                              text_color=root_object.color_bank['dark'].loc[
                                                                  'text_color'],
                                                              fg_color=root_object.color_bank['dark'].loc[
                                                                  'darker_widget_color'],
                                                              hover_color=root_object.color_bank['dark'].loc[
                                                                  'hover_color'],
                                                              corner_radius=0,
                                                              border_width=3,
                                                              border_color=root_object.color_bank['dark'].loc[
                                                                  'border_color'],
                                                              command=lambda: self.csv_reading_process_after_pressing_submit_all_button(
                                                                  root_object)
                                                              )

                self.convert_to_gpd_df_button = ctk.CTkButton(root_object.grid_frame,
                                                              text="Convert data to GeoPandas DataFrame",
                                                              height=30,
                                                              width=100,
                                                              font=root_object.smaller_font_props,
                                                              text_color=root_object.color_bank['dark'].loc[
                                                                  'text_color'],
                                                              fg_color=root_object.color_bank['dark'].loc[
                                                                  'darker_widget_color'],
                                                              hover_color=root_object.color_bank['dark'].loc[
                                                                  'hover_color'],
                                                              corner_radius=0,
                                                              border_width=3,
                                                              border_color=root_object.color_bank['dark'].loc[
                                                                  'border_color'],
                                                              command=lambda: self.convert_to_gpd_df_action(root_object)
                                                              )

                self.choose_another_dataset_button = ctk.CTkButton(root_object.grid_frame,
                                                                   text="Save the dataset and choose another one.",
                                                                   height=30,
                                                                   width=100,
                                                                   font=root_object.smaller_font_props,
                                                                   text_color=root_object.color_bank['dark'].loc[
                                                                       'text_color'],
                                                                   fg_color=root_object.color_bank['dark'].loc[
                                                                       'darker_widget_color'],
                                                                   hover_color=root_object.color_bank['dark'].loc[
                                                                       'hover_color'],
                                                                   corner_radius=0,
                                                                   border_width=3,
                                                                   border_color=root_object.color_bank['dark'].loc[
                                                                       'border_color'],
                                                                   command=lambda: self.logged_in_screen_with_datasets_after_choosing_first_dataset(
                                                                       root_object=root_object)
                                                                   )

                self.geospatial_visualization_frame = ctk.CTkFrame(root_object,
                                                                   height=400,
                                                                   width=800,
                                                                   fg_color=root_object.color_bank['dark'].loc[
                                                                       'background_color'],
                                                                   corner_radius=0
                                                                   )

                self.geospatial_visualization_options_frame = ctk.CTkFrame(root_object,
                                                                           height=400,
                                                                           width=400,
                                                                           fg_color=root_object.color_bank['dark'].loc[
                                                                               'background_color'],
                                                                           corner_radius=0
                                                                           )

                colors_list = ["red", "green", "blue", "black", "white", "orange"]
                self.color_combo_box = ctk.CTkComboBox(self.geospatial_visualization_options_frame,
                                                       state="readonly",
                                                       width=160,
                                                       height=40,
                                                       fg_color=root_object.color_bank['dark'].loc[
                                                           'darker_widget_color'],
                                                       button_color=root_object.color_bank['dark'].loc[
                                                           'darker_widget_color'],
                                                       corner_radius=0,
                                                       values=colors_list,
                                                       command=lambda new_color_value: self.set_color_value(
                                                           new_color_value)
                                                       )

                self.edge_color_combo_box = ctk.CTkComboBox(self.geospatial_visualization_options_frame,
                                                            state="readonly",
                                                            width=160,
                                                            height=40,
                                                            fg_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            button_color=root_object.color_bank['dark'].loc[
                                                                'darker_widget_color'],
                                                            corner_radius=0,
                                                            values=colors_list,
                                                            command=lambda new_color_value: self.set_edge_color_value(
                                                                new_color_value)
                                                            )

                self.x_parameter_combo_box = ctk.CTkComboBox(root_object,
                                                             state="readonly",
                                                             width=300,
                                                             height=40,
                                                             fg_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             button_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             corner_radius=0,
                                                             command=lambda x_parameter: self.set_x_parameter(
                                                                 x_parameter)
                                                             )

                self.y_parameter_combo_box = ctk.CTkComboBox(root_object,
                                                             state="readonly",
                                                             width=300,
                                                             height=40,
                                                             fg_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             button_color=root_object.color_bank['dark'].loc[
                                                                 'darker_widget_color'],
                                                             corner_radius=0,
                                                             command=lambda y_parameter: self.set_y_parameter(
                                                                 y_parameter)
                                                             )

                self.submit_all_and_visualize_geospatial_button = ctk.CTkButton(
                    self.geospatial_visualization_options_frame,
                    text="Submit every parameter and visualize",
                    height=30,
                    width=100,
                    font=root_object.smaller_font_props,
                    text_color=
                    root_object.color_bank['dark'].loc[
                        'text_color'],
                    fg_color=
                    root_object.color_bank['dark'].loc[
                        'darker_widget_color'],
                    hover_color=
                    root_object.color_bank['dark'].loc[
                        'hover_color'],
                    corner_radius=0,
                    border_width=3,
                    border_color=
                    root_object.color_bank['dark'].loc[
                        'border_color'],
                    command=lambda: self.submit_all_parameters_and_visualize_geospatial_action()
                )

                self.conversion_to_gpd_label = ctk.CTkLabel(root_object,
                                                            text="",
                                                            font=root_object.bigger_font_props,
                                                            text_color=root_object.color_bank['dark'].loc['text_color']
                                                            )

            def set_x_parameter(self, x_value):
                setattr(self, "column_to_be_x_parameter_to_gpd_conversion", x_value)

            def set_y_parameter(self, y_value):
                setattr(self, "column_to_be_y_parameter_to_gpd_conversion", y_value)

            def submit_all_and_go_to_visualize_geospatial_action(self):
                self.data_frame.content.plot()

            def set_color_value(self, new_value):
                self.color_value = new_value

            def set_edge_color_value(self, new_value):
                self.border_color_value = new_value

            def replace_classic_visualization_with_geospatial_visualization(self, root_object):
                self.conversion_to_gpd_label.pack(pady=10)
                try:
                    self.geo_pandas_data_frame = gpd.GeoDataFrame(self.data_frame.content,
                                                                  geometry=gpd.points_from_xy(self.data_frame.content[
                                                                                                  self.column_to_be_x_parameter_to_gpd_conversion],
                                                                                              self.data_frame.content[
                                                                                                  self.column_to_be_y_parameter_to_gpd_conversion]
                                                                                              )
                                                                  )
                except KeyError and ValueError:
                    self.conversion_to_gpd_label.configure(
                        text=f"Conversion to GeoPandas DataFrame failed.\nUnable to convert columns \n x - {self.column_to_be_x_parameter_to_gpd_conversion}\n and y - {self.column_to_be_y_parameter_to_gpd_conversion} to vertical points.")
                    return False

                self.data_table = Table(parent=self.geospatial_visualization_frame, dataframe=self.data_frame.content)
                self.geospatial_visualization_frame.pack(pady=10)
                self.geospatial_visualization_options_frame.pack(pady=10)
                root_object.grid_frame.pack_forget()
                self.geospatial_visualization_button.pack_forget()
                self.data_table_frame.pack_forget()
                self.data_table.show()
                self.edge_color_combo_box.grid(row=0, column=1)
                self.color_combo_box.grid(row=0, column=0)
                self.pick_random_colors_map_button.grid(row=0, column=2)
                self.submit_all_and_visualize_geospatial_button.grid(row=4, column=1)
                self.edge_color_combo_box.set("Edge color:")
                self.color_combo_box.set("Object color:")

            def convert_to_gpd_df_action(self, root_object):
                root_object.grid_frame.pack_forget()
                self.x_parameter_combo_box.configure(values=self.data_frame.content.columns)
                self.x_parameter_combo_box.set("Pick column that has x coordinates")
                self.y_parameter_combo_box.configure(values=self.data_frame.content.columns)
                self.y_parameter_combo_box.set("Pick column that has y coordinates")
                self.x_parameter_combo_box.pack(pady=10)
                self.y_parameter_combo_box.pack(pady=10)
                self.geospatial_visualization_button.pack(pady=10)

            def csv_reading_process_after_pressing_submit_all_button(self, root_object):
                self.dictionary_of_read_csv_arguments = {
                    "encoding": root_object.data_frame.encoding,
                    "low_memory": self.low_memory_argument.get(),
                }
                if hasattr(self, "quote_char"):
                    self.dictionary_of_read_csv_arguments["quotechar"] = self.quote_char.replace(' ', '')
                if hasattr(root_object.data_frame, "separator"):
                    self.dictionary_of_read_csv_arguments["delimiter"] = root_object.data_frame.separator
                if hasattr(self, "selected_columns_checkboxes_to_usecols"):
                    self.dictionary_of_read_csv_arguments[
                        "usecols"] = self.dictionary_of_columns_to_become_index_checkboxes.keys()

                self.data_frame = DataFrameAndItsProperties()
                self.data_frame.content = pd.read_csv(root_object.data_frame.file_path,
                                                      **self.dictionary_of_read_csv_arguments)
                self.table_including_operational_dataframe = Table(self.data_table_frame,
                                                                   dataframe=self.data_frame.content)
                self.table_including_operational_dataframe.show()
                self.data_frames_list.append(self.data_frame.content)
                self.convert_to_gpd_df_button.grid(column=0, row=2)

            def make_checkboxes_for_each_chosen_column_to_become_index(self, root_object):
                for column_name, is_column_checked in self.selected_columns_checkboxes_to_usecols.items():
                    if is_column_checked == 1:
                        column_variable = ctk.IntVar()
                        column_checkbox = ctk.CTkCheckBox(self.columns_to_choose_to_become_index_scroll_frame,
                                                          text=f"{column_name}",
                                                          height=20,
                                                          width=100,
                                                          font=root_object.smaller_font_props,
                                                          text_color=root_object.color_bank['dark'].loc['text_color'],
                                                          fg_color=root_object.color_bank['dark'].loc[
                                                              'darker_widget_color'],
                                                          hover_color=root_object.color_bank['dark'].loc['hover_color'],
                                                          corner_radius=10,
                                                          border_width=3,
                                                          border_color=root_object.color_bank['dark'].loc[
                                                              'border_color'],
                                                          variable=column_variable,
                                                          onvalue=1,
                                                          offvalue=0
                                                          )

                        self.dictionary_of_columns_to_become_index_checkboxes[column_name] = [column_checkbox,
                                                                                              column_variable]
                        root_object.all_widgets.append(column_checkbox)

            @staticmethod
            def action_after_choosing_quote_char(quote_char_chosen_from_combobox: str,
                                                 data_frame_properties) -> None:
                data_frame_properties.quote_char = quote_char_chosen_from_combobox

            @staticmethod
            def action_after_choosing_separator(separator_chosen_from_combobox: str,
                                                data_frame_properties) -> None:
                data_frame_properties.separator = separator_chosen_from_combobox

            def replace_select_columns_button_with_columns_choose_frame(self) -> None:
                self.optionally_select_columns_button.grid_forget()
                self.columns_to_choose_to_become_usecols_scroll_frame.grid(row=0, column=1, sticky='nswe')
                self.submit_columns_to_become_in_usecols_argument_button.grid(row=1, column=1, sticky='nwe')
                self.place_ctk_objects_from_dictionary(self.dictionary_of_columns_checkboxes)

            def submit_columns_to_become_in_usecols_argument_action(self, root_object) -> None:
                self.columns_to_choose_to_become_index_scroll_frame.grid(row=2, column=1)

                for column_name, column_checkbox_to_variable_value in self.dictionary_of_columns_checkboxes.items():
                    is_column_chosen_int_value = column_checkbox_to_variable_value[1].get()
                    self.selected_columns_checkboxes_to_usecols[column_name] = is_column_chosen_int_value

                self.make_checkboxes_for_each_chosen_column_to_become_index(root_object=root_object)
                self.place_ctk_objects_from_dictionary(
                    dictionary_with_any_ctk_objects=self.dictionary_of_columns_to_become_index_checkboxes
                )

            def make_checkboxes_for_every_column(self, dataframe_utilities, root_object) -> None:
                dataframe_sample_columns = dataframe_utilities.content.columns
                for column_name in dataframe_sample_columns:
                    column_variable = ctk.IntVar()
                    column_checkbox = ctk.CTkCheckBox(self.columns_to_choose_to_become_usecols_scroll_frame,
                                                      text=f"{column_name}",
                                                      height=20,
                                                      width=100,
                                                      font=root_object.smaller_font_props,
                                                      text_color=root_object.color_bank['dark'].loc['text_color'],
                                                      fg_color=root_object.color_bank['dark'].loc[
                                                          'darker_widget_color'],
                                                      hover_color=root_object.color_bank['dark'].loc['hover_color'],
                                                      corner_radius=10,
                                                      border_width=3,
                                                      border_color=root_object.color_bank['dark'].loc['border_color'],
                                                      variable=column_variable,
                                                      onvalue=1,
                                                      offvalue=0
                                                      )

                    self.dictionary_of_columns_checkboxes[column_name] = [column_checkbox, column_variable]

                    root_object.all_widgets.append(column_checkbox)

            @staticmethod
            def place_ctk_objects_from_dictionary(dictionary_with_any_ctk_objects) -> None:
                for column_checkbox_data in dictionary_with_any_ctk_objects.values():
                    checkbox_object = column_checkbox_data[0]
                    checkbox_object.pack(pady=10, anchor='w')

            def logged_in_screen_with_datasets_after_choosing_first_dataset(self, root_object):
                root_object.grid_frame.pack_forget()
                self.data_table_frame.pack_forget()
                root_object.logged_in_screen_process()

        class DataFrameAndItsProperties:
            def __init__(self, name="", file_path="", data_frame_object="", separator=",", encoding="utf-8"):
                self.name = name
                self.file_path = file_path
                self.content = data_frame_object
                self.separator = separator
                self.encoding = encoding

        self.data_frame = DataFrameAndItsProperties()

        self.import_users_data_frame = ctk.CTkFrame(self,
                                                    height=600,
                                                    width=800,
                                                    fg_color=self.color_bank['dark'].loc['background_color'],
                                                    corner_radius=5
                                                    )

        self.confirm_data_importing_process_button = ctk.CTkButton(self.import_users_data_frame,
                                                                   height=50,
                                                                   width=100,
                                                                   font=self.smaller_font_props,
                                                                   corner_radius=5,
                                                                   text_color=self.color_bank['dark'].loc[
                                                                       'text_color'],
                                                                   fg_color=self.color_bank['dark'].loc[
                                                                       'darker_widget_color'],
                                                                   hover_color=self.color_bank['dark'].loc[
                                                                       'darker_widget_color'],
                                                                   border_color=self.color_bank['dark'].loc[
                                                                       'border_color'],
                                                                   text='Process import',
                                                                   command=self.process_imports
                                                                   )

        self.grid_frame = ctk.CTkFrame(self,
                                       height=400,
                                       width=1200,
                                       fg_color=self.color_bank['dark'].loc['background_color'],
                                       corner_radius=0
                                       )

        self.grid_frame_containing_csv_options_utilities = GridFrameContainingCsvOptionsUtilities(root_object=self)
        self.grid_frame.columnconfigure(index=(0, 1, 2, 3, 4, 5), weight=1)  # 6 columns
        self.grid_frame.rowconfigure(index=(0, 1, 2), weight=1)  # 3 rows

        self.all_widgets = [self.login_frame_utilities.login_entry,
                            self.login_frame_utilities.password_entry,
                            self.login_frame_utilities.appearance_color_switch,
                            self.login_frame_utilities.fullscreen_switch,
                            self.login_frame_utilities.enter_as_guest_button,
                            self.login_frame_utilities.submit_button,
                            self.login_frame_utilities.remember_me_checkbox,
                            self.login_frame_utilities.login_process_execution_label,
                            self.example_plot_and_chart_choice_frame_utilities.which_year_combo_box,
                            self.example_plot_and_chart_choice_frame_utilities.which_year_label,
                            self.example_plot_and_chart_choice_frame_utilities.back_to_login_screen_button,
                            self.grid_frame_containing_csv_options_utilities.optionally_select_columns_button,
                            self.grid_frame_containing_csv_options_utilities.low_memory_switch,
                            self.grid_frame_containing_csv_options_utilities.submit_columns_to_become_in_usecols_argument_button,
                            self.grid_frame_containing_csv_options_utilities.separators_combo_box]

        self.all_frames = [self.login_frame, self.plot_frame, self.chart_choice_frame,
                           self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.datasets_scrollable_frame,
                           self.grid_frame,
                           self.grid_frame_containing_csv_options_utilities.columns_to_choose_to_become_usecols_scroll_frame,
                           self.grid_frame_containing_csv_options_utilities.columns_to_choose_to_become_index_scroll_frame]

        self.try_to_get_remember_me_processed_or_display_login_screen(db_object)

    def is_figure_defined_if_no_then_define_it_and_create_canvas_widget(self,
                                                                        interface_object,
                                                                        frame_to_plot_canvas_on,
                                                                        root_object):
        if not hasattr(interface_object, 'fig'):
            interface_object.fig = Figure(dpi=100,
                                          facecolor=root_object.color_bank['dark']['darker_widget_color'],
                                          figsize=(16, 10)
                                          )
            interface_object.ax = interface_object.fig.add_subplot(111)

            interface_object.canvas = FigureCanvasTkAgg(interface_object.fig,
                                                        master=getattr(root_object,
                                                                       frame_to_plot_canvas_on)
                                                        )
            interface_object.canvas_widget = interface_object.canvas.get_tk_widget()
            interface_object.canvas_widget.pack(pady=10)
        else:
            interface_object.ax.clear()

    def process_imports(self):
        users_data_file = pd.read_excel(io=self.import_xlsx_file_path)
        logins = users_data_file["Login"]
        self.db_object.cursor.execute(
            """INSERT INTO users_login_and_pass
            (username, password) VALUES (?, ?)""",
            (logins, users_data_file["Password"])
        )

        self.db_object.cursor.execute(
            """INSERT INTO users_rights 
            (username, rights) VALUES (?, ?)""",
            (logins, users_data_file["Power"])
        )
        del users_data_file, logins, users_data_file

    def try_to_get_remember_me_processed_or_display_login_screen(self, db_object: db_connection.Db) -> None:
        username_or_null_if_not_found = db_object._get_remembered()
        match isinstance(username_or_null_if_not_found[0], str):
            case False:
                self.pack_login_frame()
                self.login_frame_utilities.pack_widgets()

            case True:
                rights = db_object._get_rights(username_or_null_if_not_found)
                self.logged_in_screen_process()
                match rights:
                    case "admin":
                        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.import_users_data_button.pack()

                    case _:
                        pass

    def csv_processing_screen(self, file_path: str) -> None:
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button.pack_forget()
        self.grid_frame.pack(pady=20)
        self.grid_frame_containing_csv_options_utilities.data_table_frame.pack(pady=10)
        self.grid_frame_containing_csv_options_utilities.low_memory_switch.grid(row=0, column=0, sticky='nwe')
        self.grid_frame_containing_csv_options_utilities.optionally_select_columns_button.grid(row=0, column=1,
                                                                                               sticky='nswe')
        self.grid_frame_containing_csv_options_utilities.separators_combo_box.grid(row=0, column=3, sticky='nwe')
        self.grid_frame_containing_csv_options_utilities.separators_combo_box.set("Separator (default comma):")
        self.grid_frame_containing_csv_options_utilities.quote_char_combobox.grid(row=0, column=4, sticky='nwe')
        self.grid_frame_containing_csv_options_utilities.quote_char_combobox.set("Quote char (default none): ")
        self.grid_frame_containing_csv_options_utilities.submit_everything_button.grid(row=1, column=4)
        self.grid_frame_containing_csv_options_utilities.choose_another_dataset_button.grid(row=2, column=4,
                                                                                            sticky='nwe')

        with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        with open(file_path, 'r') as file:
            content_list = []
            for i in range(10):
                content_list.append(file.readline())

        possible_delimiters_dictionary = {";": 0, ",": 0, "\t": 0, "\n": 0, "-": 0}
        for row in content_list:
            for char in row:
                if char in possible_delimiters_dictionary.keys():
                    possible_delimiters_dictionary[char] += 1

        separator_occurrences = 0
        separator_argument = ','

        for delimiter, occurrences in possible_delimiters_dictionary.items():
            if occurrences > separator_occurrences:
                separator_argument = delimiter
                separator_occurrences = occurrences

        self.grid_frame_containing_csv_options_utilities.separators_combo_box.set(
            f"Detected sep='{separator_argument}'")
        df_content = pd.read_csv(
            filepath_or_buffer=file_path,
            sep=separator_argument,
            encoding=encoding
        )

        self.data_frame.file_path = file_path
        self.data_frame.content = df_content
        self.data_frame.separator = separator_argument
        self.data_frame.encoding = encoding
        self.grid_frame_containing_csv_options_utilities.make_checkboxes_for_every_column(
            dataframe_utilities=self.data_frame,
            root_object=self
        )

    @staticmethod
    def pack_forget_visible_elements(visible_elements_iterable=None) -> None:
        if visible_elements_iterable is None:
            visible_elements_iterable = []
        match isinstance(visible_elements_iterable, (list, tuple)):
            case True:
                for visible_object in visible_elements_iterable:
                    visible_object.pack_forget()
            case _:
                visible_elements_iterable.pack_forget()

    def logged_in_screen_process(self) -> None:
        self.login_frame.pack_forget()
        self.clear_entries()
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button.pack(pady=5)
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.datasets_scrollable_frame.pack(
            pady=25)
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.back_to_login_screen_from_datasets_choosing_button.pack(
            pady=10)
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.back_to_login_screen_from_datasets_choosing_button.pack_propagate(
            False)
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.create_buttons_of_datasets(
            datasets_names=datasets.dictionary_of_dataset_name_and_its_path, root_object=self
        )
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.set_command_for_datasets_buttons(
            root_object=self)
        self.frame_including_datasets_scrollable_frame_and_back_to_login_button_utilities.pack_datasets_buttons_on_scrollable_frame()

    def clear_entries(self, which_entry=None) -> None:
        match type(which_entry):
            case ctk.CTkEntry:
                which_entry.delete(0, ctk.END)
            case None:
                for entry in self.login_frame_utilities.login_process_entries:
                    entry.delete(0, ctk.END)

    def pack_login_frame(self):
        self.login_frame.pack_propagate(False)
        self.login_frame.pack(pady=10, anchor='center')

    def freeze_login_processors(self) -> None:
        self.login_frame_utilities.login_process_execution_label.configure(
            text="Too many login attempts, process suspended for 5 minutes")
        self.login_frame_utilities.submit_button.configure(state="disabled")

        for entry in self.login_frame_utilities.login_process_entries:
            entry.configure(state='disabled')
            self.after(300000, lambda: entry.configure(state="normal"))

        self.after(300000, lambda: self.login_frame_utilities.configure(state='normal'))


class Datasets:
    def __init__(self, path_of_sets: str):
        self.files_to_ignore_list = ["shx", "cpg", "dbf", "prj", "sbn", "sbx", "xml"]
        self.list_of_datasets_names_with_extension = [filename for filename in listdir(path_of_sets) if
                                                      filename.split(".")[-1] not in self.files_to_ignore_list]
        self.dictionary_of_dataset_name_and_its_path = {filename: (path_of_sets + filename) for
                                                        filename in self.list_of_datasets_names_with_extension if
                                                        filename.split(".")[-1] not in self.files_to_ignore_list}


db = db_connection.Db()
datasets_path = 'C:/Users/adria/PycharmProjects/GeoAnalitycsDesktopApp/.venv/data/data_sets/'
datasets = Datasets(datasets_path)
applicationScreen = ApplicationScreenRoot(db)
applicationScreen.mainloop()
