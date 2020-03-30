from ..pages.login_page import LoginPage
from ..pages.track_page import TrackPage
from ..utils.test_staus import TestStatus
from ..config import read_config as rd
import unittest
import pytest
import allure


@pytest.mark.usefixtures("set_up", "one_time_set_up")
class TrackPageTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self):
        self.loginPage = LoginPage(self.driver)
        self.trackPage = TrackPage(self.driver)
        self.ts = TestStatus(self.driver)

    @allure.story("POC scope")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test sum of streams on a track page")
    @allure.description("Check that user is able to get streams data for custom dates period with deeplinks")
    def test_sum_of_streams_on_a_track_page(self):
        self.loginPage.login(rd.get_config('user_email'), rd.get_config('user_password'))
        self.loginPage.is_logged_in()

        self.trackPage.open_spotify_track_page(rd.get_config('spotify_trackId'))
        self.trackPage.select_market("Australia")
        self.trackPage.select_dsp("Apple Music")
        self.trackPage.select_previous_mounth_period()

        self.ts.markFinal(self.trackPage.are_start_dates_match(), "Start dates are matching")
        self.ts.markFinal(self.trackPage.are_end_dates_match(), "End dates are matching")

    @allure.story("POC scope")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Tooltip verification in Track performance section for Apple DSP 1 day period")
    @allure.description("comparing of ‘Total’ in tooltip with 'Streams in period' in legend (negative case – "
                        "known issue, streams total are not equal")
    def test_tooltip_total_on_a_track_page(self):
        self.loginPage.login(rd.get_config('user_email'), rd.get_config('user_password'))
        self.loginPage.is_logged_in()

        self.trackPage.open_spotify_track_page(rd.get_config('spotify_trackId'))
        self.trackPage.select_market("Australia")
        self.trackPage.select_dsp("Apple Music")

        self.trackPage.select_one_day_period_in_previous_month()
        tooltip_total = self.trackPage.get_tooltip_total()
        graph_total = self.trackPage.get_streams_in_period_total()

        self.ts.markFinal(self.trackPage.are_graph_total_and_tooltip_match(tooltip_total, graph_total), "Totals are matching")

    @allure.story("POC scope")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Check that user is able to get data for one year using date quick filter")
    @allure.description("Track performance graph for 1Y period – data loading")
    def test_graph_selection_for_one_year(self):
        self.loginPage.login(rd.get_config('user_email'), rd.get_config('user_password'))
        self.loginPage.is_logged_in()

        self.trackPage.open_spotify_track_page(rd.get_config('spotify_trackId'))
        self.trackPage.select_market("Australia")
        self.trackPage.select_dsp("Apple Music")

        self.trackPage.select_graph_one_year_period()
        graph_period = self.trackPage.get_graph_period_displayed()

        self.ts.markFinal(self.trackPage.is_graph_period_correct(graph_period, 365),
                          "Graph period is valid")

    @allure.story("POC scope")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Legend in Track Performance: ‘Lean back’ + ’Lean forward’ ")
    @allure.description("Legend in Track Performance: ‘Lean back’ + ’Lean forward’ should be equal to 100%")
    def test_lenend_lean_back_lean_forward(self):
        self.loginPage.login(rd.get_config('user_email'), rd.get_config('user_password'))
        self.loginPage.is_logged_in()

        self.trackPage.open_spotify_track_page(rd.get_config('spotify_trackId'))
        self.trackPage.select_market("Australia")
        self.trackPage.select_dsp("Spotify")

        lean_back = self.trackPage.get_lean_back_values()
        lean_forward = self.trackPage.get_lean_forward_values()

        self.ts.markFinal(self.trackPage.are_lean_froward_and_back_100(lean_back, lean_forward), "Values sum is 100%")



