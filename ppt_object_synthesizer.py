from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Emu
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
        shape_type = random.choice(list(self.shapes.items()))
        self.prs.slides[-1].shapes.add_shape(
            shape_type[1], 
            Inches(1), Inches(1), Inches(1),  Inches(1)
        )

        shape = self.prs.slides[-1].shapes[-1]

        for property, value_range in self.base_shape_visual_property_range.items():
            setattr(shape, property, random.randint(*value_range))

        
        return shape

    def save(self):
        self.prs.save('ppt_object_dataset.pptx')


ppt = PPT()
ppt.add_blank_slide()
for i in range(10):
    ppt.generate_random_shape()
ppt.save()