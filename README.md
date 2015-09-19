# SteganEnc

##### This piece of code aims at helping users to hide information (textual data, in this case) within images without any lose of data or change in view of the image 

#####How to use this :<br>
  1. <h5>Setting up environment</h5>
    1. Please enter `pip -r install Requirements.txt`, after you have moved into the directory containing the requirements.txt file
    2. This ensures that the SteganEnc.py functions properly, as depedencies are downloaded and ready to use.
  2. <h5>Running the SteganEnc.py code</h5> 
    1. <h6>For encoding text into image</h6>
      1. Please enter `python SteganEnc.py [-force] [Image_Source] [Text_Source] [Image_Destination]`
      2. `[-force]` is used to bypass all warnings, which happens in the case that the image already contains encoded data
      3. `[Image_Source]` refers to the location containing the image which is going to be used for encoding data into it
      4. `[Text_Source]` refers to location containing the textfile, which contains the text that needs to be encoded
      5. `[Image_Destination]` is an optional parameter, refers to the location to which the encoded image has to be stored. For eg: 'documents/Images/encoded_image.png'
      6. Note: It is always prefered to save the encoded image in .png format
    2. <h6>For decoding an encoded image</h6>
      1.  Please enter `python SteganEnc.py [-decode] [Image_Source] `
      2.  `[-decode]` as the term suggests, it specifies the program to run a decode operation 
      3.  `[Image_Source]` refers to the location containing the image from which data has to be extracted
  3. <h5>Enjoy :)</h5>    
  
##### Feel free to provide updates or enhancements
  
      
      
      
  
  
