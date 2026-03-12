import pypandoc

def convert_epub_to_pdf(epub_file, pdf_file):
    pypandoc.convert_file(epub_file, 'pdf', outputfile=pdf_file, extra_args=['--pdf-engine=xelatex'])

convert_epub_to_pdf("C:\\Users\\EMMANUEL\\Documents\\Projects\\Vault\\h.epub", "C:\\Users\\EMMANUEL\\Documents\\Projects\\Vault\\Achebe, Chinua - There Was a Country (2012, Penguin Publishing Group) - libgen.li.pdf")
