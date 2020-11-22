import unittest

from raspberry_home.view.geometry import Point
from raspberry_home.view.stack import HorizontalStack, StackDistribution, StackAlignment, VerticalStack
from raspberry_home.view.text import Text, Size
from tests.MagicView import MagicView


class TestStack(unittest.TestCase):

    def setUp(self):
        MagicView.reset()

    def test_horizontal_spacing_ten_dist_start_align_start(self):
        MagicView.test_render(
            container_size=Size(200, 200),
            root_view=HorizontalStack(
                children=[
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(200, 200),
                        expected_origin=Point(0, 0),
                    ).named("first view"),
                    MagicView(
                        content_size=Size(100, 100),
                        expected_container_size=Size(140, 200),
                        expected_origin=Point(60, 0),
                    ).named("second view"),
                ],
                spacing=10,
                distribution=StackDistribution.Start,
                alignment=StackAlignment.Start
            ),
            expected_content_size=Size(160, 100),
        )

    def test_horizontal_spacing_ten_dist_start_align_end(self):
        MagicView.test_render(
            container_size=Size(200, 200),
            root_view=HorizontalStack(
                children=[
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(200, 200),
                        expected_origin=Point(0, 50),
                    ).named("first view"),
                    MagicView(
                        content_size=Size(100, 100),
                        expected_container_size=Size(140, 200),
                        expected_origin=Point(60, 0),
                    ).named("second view"),
                ],
                spacing=10,
                distribution=StackDistribution.Start,
                alignment=StackAlignment.End
            ),
            expected_content_size=Size(160, 100),
        )

    def test_horizontal_spacing_ten_dist_start_align_center(self):
        MagicView.test_render(
            container_size=Size(200, 200),
            root_view=HorizontalStack(
                children=[
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(200, 200),
                        expected_origin=Point(0, 25),
                    ).named("first view"),
                    MagicView(
                        content_size=Size(100, 100),
                        expected_container_size=Size(140, 200),
                        expected_origin=Point(60, 0),
                    ).named("second view"),
                ],
                spacing=10,
                distribution=StackDistribution.Start,
                alignment=StackAlignment.Center
            ),
            expected_content_size=Size(160, 100),
        )

    def test_horizontal_spacing_ten_dist_end_align_start(self):
        MagicView.test_render(
            container_size=Size(200, 200),
            root_view=HorizontalStack(
                children=[
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(90, 200),
                        expected_origin=Point(40, 0),
                    ).named("first view"),
                    MagicView(
                        content_size=Size(100, 100),
                        expected_container_size=Size(200, 200),
                        expected_origin=Point(100, 0),
                    ).named("second view"),
                ],
                spacing=10,
                distribution=StackDistribution.End,
                alignment=StackAlignment.Start
            ),
            expected_content_size=Size(200, 100),
        )

    def test_horizontal_spacing_ten_dist_equal_align_start(self):
        MagicView.test_render(
            container_size=Size(200, 200),
            root_view=HorizontalStack(
                children=[
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(95, 200),
                        expected_origin=Point(0, 0),
                    ).named("first view"),
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(95, 200),
                        expected_origin=Point(105, 0),
                    ).named("second view"),
                ],
                spacing=10,
                distribution=StackDistribution.Equal,
                alignment=StackAlignment.Start
            ),
            expected_content_size=Size(200, 100),
        )

    def test_vertical_spacing_ten_dist_start_align_start(self):
        MagicView.test_render(
            container_size=Size(100, 200),
            root_view=VerticalStack(
                children=[
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(100, 200),
                        expected_origin=Point(0, 0),
                    ).named("first view"),
                    MagicView(
                        content_size=Size(50, 50),
                        expected_container_size=Size(100, 140),
                        expected_origin=Point(0, 60),
                    ).named("second view"),
                ],
                spacing=10,
                distribution=StackDistribution.Start,
                alignment=StackAlignment.Start
            ),
            expected_content_size=Size(50, 200),
        )


if __name__ == '__main__':
    unittest.main()
