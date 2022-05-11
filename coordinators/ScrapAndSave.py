from azurecomp.azure_blob_storage import upload_string_as_blob
from  webScraping import JpMorganLeaderShip

def searchAndSaveToBlobStorage(company):
    list_of_leader_info_objects=JpMorganLeaderShip.getTextAboutExec(company)
    for index, leader_info_object in enumerate(list_of_leader_info_objects):
        file_name = company+"_eid_"+str(index)+".txt"
        upload_string_as_blob(file_name, leader_info_object.text)
        for image_index,eachImage_content in enumerate(leader_info_object.image_content):
            img_file_name = company + "_img_"+str(image_index)+"_eid_" + str(index) + "."+leader_info_object.image_extn[image_index]
            upload_string_as_blob(img_file_name, eachImage_content)


if __name__=='__main__':
    searchAndSaveToBlobStorage("JpMorgan Chase")
