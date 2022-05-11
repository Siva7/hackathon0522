from azurecomp.azure_blob_storage import upload_string_as_blob
from  webScraping import JpMorganLeaderShip

def searchAndSaveToBlobStorage(company):
    leader_text_img_details=JpMorganLeaderShip.getTextAboutExec(company)
    for index, value in enumerate(leader_text_img_details):
        text_content,leader_img_list=value
        file_name = company+"_eid_"+str(index)+".txt"
        upload_string_as_blob(file_name,text_content)
        for image_index,eachImage in enumerate(leader_img_list):
            img_file_name = company + "img_"+str(image_index)+"_eid_" + str(index) + ".jpg"
            upload_string_as_blob(img_file_name, eachImage)


if __name__=='__main__':
    searchAndSaveToBlobStorage("JpMorgan Chase")
