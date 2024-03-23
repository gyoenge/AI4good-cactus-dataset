from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE
# from pptx.enum.dml import MSO_FILL
from pptx.util import Inches
import random

class PPT:
    def __init__(self):
        self.prs = Presentation()

        self.prs.slide_width = Inches(8)
        self.prs.slide_height = Inches(6)

        self.prs.core_properties.author = "Cactus"
        self.prs.core_properties.category = "Image Dataset"
        self.prs.core_properties.comments = "This is a ppt file of randomly synthesized ppt shapes. It will be the dataset for training custom ppt object detection model. "
        self.prs.core_properties.title = "PPT Object Dataset"

        self.prs.core_properties.version = "0.0"

        self.shapes = dict((member.name, member.value) for member in MSO_SHAPE.__members__)

        self.lines = dict((member.name, member.value) for member in MSO_LINE.__members__ if member.name != "DASH_STYLE_MIXED") # DASH_STYLE_MIXED is not supported by python-pptx

        shape_max_size = (Inches(4), Inches(4))
        self.base_shape_visual_property_range = {
            "left": (0, self.prs.slide_width - shape_max_size[0]), 
            "top": (0, self.prs.slide_height - shape_max_size[1]), 
            "width": (0, shape_max_size[0]), 
            "height": (0, shape_max_size[1]), 
            "rotation": (0, 360), 
        }
    
    def add_blank_slide(self):
        self.prs.slides.add_slide(self.prs.slide_layouts.get_by_name("Blank"))
        
    def generate_random_shape(self):
        shapes = random.choice(list(self.shapes.items()))
        self.prs.slides[-1].shapes.add_shape(
            shapes[1], 
            Inches(1), Inches(1), Inches(1),  Inches(1)
        )

        shape = self.prs.slides[-1].shapes[-1]

        for property, value_range in self.base_shape_visual_property_range.items():
            setattr(shape, property, random.randint(*value_range))

        shape.fill.solid()
        shape.fill.fore_color.rgb = self._generate_random_rgb_color()
        shape.line.color.rgb = self._generate_random_rgb_color()
        shape.line.dash_style = random.choice(list(self.lines.values()))
        shape.line.width = Inches(random.randrange(0, 1))
        
        return shape
    
    def _generate_random_rgb_color(self):
        return RGBColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def save(self):
        self.prs.save('ppt_object_dataset.pptx')


ppt = PPT()
ppt.add_blank_slide()
for i in range(5):
    ppt.generate_random_shape()
ppt.save()