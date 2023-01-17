import gdown
def verify_link(link):
    if link is None or link == "":
        return "UNUSED"
    if "drive.google.com" not in link:
        return False
    if "file" not in link:
        return False
    if '/d/' not in link:
        return False
    
    id = link.split('/d/')[1].split('/')[0]
    return id

if __name__ == "__main__":
    verify_link("https://drive.google.com/file/d/1otfwuIPuvnCKyKbk--y_ZZ0kZd1ET4Nu/view?usp=sharing")