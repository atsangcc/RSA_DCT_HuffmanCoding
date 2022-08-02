# Tsang Chun Ching , Student#ID : 19047052G
# COMP5422 Individual Assignment
# Topic : Image Encryption by RSA Algorithm upon Image Compression by DCT and Huffman Coding
# Sender's Side Application
# July - 19 - 2022

from datetime import datetime
from myFolder.KeysFolder import PrimeGenerator

import myFolder.KeysFolder.rsaTest as rsaTest 
# the library of rsaTest is come from 
# https://gist.github.com/ErbaAitbayev/8f491c04af5fc1874e2b0744965a732b#file-rsa-py


from JpegMaster import Algoritmo_jpeg
from JpegMaster import generador_huffman_code
# the library of JpegMaster is come from 
# https://github.com/josgard94/JPEG
# Algoritmo_jpeg is for converting a 256x256 color image into a gray image and then a DCT image. 







def senderRsaKeyPair():

   primeP, primeQ= PrimeGenerator.generateTwoPrimes()

   publicKey, privateKey = rsaTest.generate_keypair(primeP, primeQ)

   # print("publicKey :")   
   # print(publicKey)
   # print("privateKey :")
   # print(privateKey)

   puFile = open("./myFolder/KeysFolder/publicKey.txt","w")
   puFile.write(str(publicKey))
   puFile.close()


   pvFile = open("./myFolder/KeysFolder/privateKey.txt","w")
   pvFile.write(str(privateKey))
   pvFile.close()

def RGB256x256_to_Huffcode(originalImgPath):
   # pass an 256X256 rgb image to "Algoritmo_jpeg.rgb256x256toDCT"
   # it shall return a txt file equivalent to the DCT image
   matrixDCT , probabilityDCT , imgDCT = Algoritmo_jpeg.rgb256x256toDCT(originalImgPath)
   # print(matrixDCT);
   # !!! Limitation : "Algoritmo_jpeg" only supports the rgb256x256 images  !!!

### ### ### ### ### ### SAVING DCT INTRIM OUTPUT ### ### ### ### ### ### 
   dctTxtPath = "./myFolder/ImgFolder/OutputImages/dct.txt" ;
   dctFile = open(dctTxtPath,"w")
   dctFile.write(matrixDCT)
   dctFile.close()
   probabilityResultPath = "./myFolder/ImgFolder/OutputImages/result.txt"
   probaFile = open(probabilityResultPath,"w")
   probaFile.write(probabilityDCT)
   probaFile.close()
   imgDCT.save("./myFolder/ImgFolder/OutputImages/dct.jpg")
### ### ### ### ### ### SAVING DCT INTRIM OUTPUT  : DONE ### ### ### ### ### ### 
   huffmanEncoderTable , imageHuffmanCodeText = generador_huffman_code.compresor_huffman(probabilityResultPath,dctTxtPath)
   now = datetime.now()
   huffmanCodeWithTimestamp = imageHuffmanCodeText+now.strftime("%m/%d/%Y , %H:%M:%S")

### ### ### ### ### ### SAVING Huffman OUTPUT ### ### ### ### ### ### 
   huffmanEncoderTablePath = "./myFolder/HuffmanFolder/codigos.txt"
   encoderFile = open(huffmanEncoderTablePath,"w")
   encoderFile.write(huffmanEncoderTable)
   encoderFile.close()

   huffmanCodeTimeList=[imageHuffmanCodeText,now.strftime("%m/%d/%Y , %H:%M:%S")]
   imgCodePath = "./myFolder/HuffmanFolder/imgHuffmanCode.txt"
   with open(imgCodePath,"w") as hCodeFile:
      for atb in huffmanCodeTimeList:
       hCodeFile.write("%s\n" % atb)
      hCodeFile.close()
### ### ### ### ### ### SAVING Huffman OUTPUT  : DONE ### ### ### ### ### ### 
   return huffmanCodeWithTimestamp


def senderSignatureOnHuffmanCode(imgHuffmanCodeWithTimestamp, privateKeyCertLocation):

   with open(privateKeyCertLocation) as senderPrivateCert:
      senderPrivateKey = senderPrivateCert.read()

   pv1 = senderPrivateKey[senderPrivateKey.index("(")+1:senderPrivateKey.index(",")]
   pv2 = senderPrivateKey[senderPrivateKey.index(", ")+1:senderPrivateKey.index(")")]

   # get the huffman hasehed :
   hashedHuffmancode = rsaTest.hashFunction(imgHuffmanCodeWithTimestamp)
   print("Hash Value of Image Huffman Code + Timestamp")
   print(hashedHuffmancode)

   # print("Sender Signs on the Huffman Code with Sender's private key ", senderPrivateKey ," . . .")
   encrypted_msg = rsaTest.encrypt((int(pv1),int(pv2)), hashedHuffmancode)   
   # print("The encrypted hashed message is: ")
   # print(encrypted_msg)
   senderOneTimeSignature=encrypted_msg

   oneTimeSignatureLocation = "./myFolder/HuffmanFolder/SenderOneTimeSignature.txt"
   with open(oneTimeSignatureLocation,'w') as signFile:
      for item in senderOneTimeSignature:
         signFile.write("%s\n" % item)
      signFile.close()

   senderOneTimeSignature=''.join(map(lambda x: str(x), encrypted_msg))

   return senderOneTimeSignature








def main() :

   senderRsaKeyPair()

   ## originalImg should be 256x256 :
   originalImgPath = "./myFolder/ImgFolder/InputImages/Lisa.jpeg" ;
   
   # obtain Huffman Code from the original image : 
   huffmancodeFromImgWithTimeStamp = RGB256x256_to_Huffcode(originalImgPath)



   privateKeyCertificateLocation = "./myFolder/KeysFolder/privateKey.txt"
   # Sender uses private key to sign on the "huffmancodeFromImg" and get back the one time signature :
   senderOneTimeSignature = senderSignatureOnHuffmanCode(huffmancodeFromImgWithTimeStamp, 
                                                         privateKeyCertificateLocation)

   # print("Sender's One-Time Signature on the hashed Huffman code : ")
   # print(senderOneTimeSignature)


   










main()