from email_service.summarizer import Summarizer
from email_service.email_parser.email_content_parser_interface import EmailContentParserInterface
from email_service.email_parser.neuron_parser import NeuronEmailParser
from email_service.email_parser.alpha_signal_parser import AlphaSignalParser
from email_service.email_parser.lenny_parser import LennyEmailParser
from email_service.email_parser.quastor_parser import QuastorEmailParser
from email_service.email_parser.sebastian_raschka_parser import SebastianRaschkaEmailParser
from email_service.email_parser.top_ml_paper_parser import TopMLPaperEmailParser



class ParserFactory:
    def __init__(self, summarizer: Summarizer):
        self.summarizer = summarizer

    def get_parser(self, blog_name: str, image_url: str) -> EmailContentParserInterface:
        if blog_name == "the_neuron":
            return NeuronEmailParser(self.summarizer, blog_name, image_url)
        elif blog_name == "alpha_signal":
            return AlphaSignalParser(self.summarizer, blog_name, image_url)
        elif blog_name == "lenny":
            return LennyEmailParser(self.summarizer, blog_name, image_url)
        elif blog_name == "quastor":
            return QuastorEmailParser(self.summarizer, blog_name, image_url)
        elif blog_name == "sebastian_raschka":
            return SebastianRaschkaEmailParser(self.summarizer, blog_name, image_url)
        elif blog_name == "top_ml_paper_of_the_week":
            return TopMLPaperEmailParser(self.summarizer, blog_name, image_url)
        else:
            print("Error: No parser found for blog type.")
