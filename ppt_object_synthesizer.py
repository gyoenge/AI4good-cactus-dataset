from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches
from random import choice

class PPT:
    def __init__(self):
        self.prs = Presentation()

        self.prs.slide_width = Inches(4)
        self.prs.slide_height = Inches(3)

        self.prs.core_properties.author = "Cactus"
        self.prs.core_properties.category = "Image Dataset"
        self.prs.core_properties.comments = "This is a ppt file of randomly synthesized ppt shapes. It will be the dataset for training custom ppt object detection model. "
        self.prs.core_properties.title = "PPT Object Dataset"

        self.prs.core_properties.version = "0.0"

        self.shapes = dict((member.name, member.value) for member in MSO_SHAPE.__members__)
    
    def add_blank_slide(self):
        self.prs.slides.add_slide(self.prs.slide_layouts.get_by_name("Blank"))
        
    def generate_random_shape(self):
        shape_type = choice(list(self.shapes.items()))
        self.prs.slides[-1].shapes.add_shape(
            shape_type[1], 
            Inches(1), Inches(1), Inches(1),  Inches(1)
        )
        shape = self.prs.slides[-1].shapes[-1]
        return shape

    def save(self):
        self.prs.save('ppt_object_dataset.pptx')


ppt = PPT()
ppt.add_blank_slide()
ppt.generate_random_shape()
ppt.save()