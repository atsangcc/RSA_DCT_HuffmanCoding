# Tsang Chun Ching , Student#ID : 19047052G
# COMP5422 Individual Assignment
# Topic : Image Encryption by RSA Algorithm upon Image Compression by DCT and Huffman Coding
# Verifier's Side Application
# July - 19 - 2022


import myFolder.KeysFolder.rsaTest as rsaTest 
# the library of rsaTest is come from 
# https://gist.github.com/ErbaAitbayev/8f491c04af5fc1874e2b0744965a732b#file-rsa-py


from JpegMaster import descompresor
from JpegMaster import idtc
# the library of JpegMaster is come from 
# https://github.com/josgard94/JPEG
# Algoritmo_jpeg is for converting a 256x256 color image into a gray image and then a DCT image. 

def unpackSenderPackage(signatureLocation,huffmancodeLocation):

    senderOneTimeSignature = []

    with open(signatureLocation) as senderSignatureFile:
      for line in senderSignatureFile:
        signatureElement = int(line[:-1])
        senderOneTimeSignature.append(signatureElement)

    huffmanCodePlusTimestamp=[]
    huffmanCodeAlone=[]
    with open(huffmancodeLocation) as huffmancodeFile:
      #   huffmanCodeAlone = huffmancodeFile.readline()
        for line in huffmancodeFile:
         huffmancodeFileLine = (line[:-1])
         huffmanCodePlusTimestamp.append(huffmancodeFileLine)
      #   for i , line in enumerate(huffmancodeFile):
      #    if i in [0,1] :
      #       huffmancodeFileLine = (line[:-1])
      #       huffmanCodeAlone.append(huffmancodeFileLine)
      #    elif i>0:
      #       break
    with open(huffmancodeLocation) as huffmancodeFile:
      huffmanCodeAlone = huffmancodeFile.readline()
         
    huffmanCodePlusTimestampString=''.join(map(lambda x: str(x), huffmanCodePlusTimestamp))
    huffmanCodeAloneString=''.join(map(lambda x: str(x), huffmanCodeAlone))

    return senderOneTimeSignature , huffmanCodePlusTimestampString , huffmanCodeAloneString

def decryptionOfSenderSignature(publicKeyCertificateLocation,senderOneTimeSignature):

    with open(publicKeyCertificateLocation) as senderPublicCert:
      senderPublicKey = senderPublicCert.read()

    pu1 = int(senderPublicKey[senderPublicKey.index("(")+1:senderPublicKey.index(",")])
    pu2 = int(senderPublicKey[senderPublicKey.index(", ")+1:senderPublicKey.index(")")])

    publicKeyJoin=(pu1,pu2)
    
    decrypted_msg = rsaTest.decrypt(publicKeyJoin, senderOneTimeSignature)   
    # print("The encrypted hashed message is: ")
    decryptedHash=''.join(map(lambda x: str(x), decrypted_msg))

    decryptedHashLocation = "./myFolder/HuffmanFolder/decryptedHash.txt"
    decryptFile = open(decryptedHashLocation,"w")
    decryptFile.write(decryptedHash)
    decryptFile.close()


    return decryptedHash

def huffmanDecoding(hEncoderPath,huffmanCodeToBeDecoded):


    print("happyhappy")
    
    recoveredDTC = descompresor.descomprimir(hEncoderPath,huffmanCodeToBeDecoded)
    
    recoveredDCTTxtPath = "./myFolder/ImgFolder/OutputImages/recovedDCT.txt"
    recDCTFile = open(recoveredDCTTxtPath,"w")
    recDCTFile.write(recoveredDTC)
    recDCTFile.close()

    return recoveredDTC , recoveredDCTTxtPath


def main():
    
    # Verifier unpacking the sender's signature and and the transmitted message 
       senderSignatureLocation = "./myFolder/HuffmanFolder/SenderOneTimeSignature.txt"
       huffmanCodeLocation =  "./myFolder/HuffmanFolder/imgHuffmanCode.txt"
       senderOneTimeSignature , receivedHuffmanCodePlusTimestamp , huffmanCodeLessTimestamp = unpackSenderPackage(senderSignatureLocation,
                                                                            huffmanCodeLocation)
      #  print("huffmanCodeLessTimestamp : ")
      #  print(huffmanCodeLessTimestamp)

       # Verifier uses Sender's Public Key to decrypt the Hashed Message from Sender's Signature
       publicKeyCertificatteLocation = "./myFolder/KeysFolder/publicKey.txt"
      #  publicKeyCertificatteLocation = "./myFolder/KeysFolder/publicKeyPrevious.txt"
       decrypted_msg = decryptionOfSenderSignature(publicKeyCertificatteLocation,senderOneTimeSignature)
       print("The decrypted HASH message is:")  
       print(decrypted_msg)

    
    # Then ,we try to verify the received huffman code against the public-key-decrypted hash message
       verificationResult = rsaTest.verify(decrypted_msg,receivedHuffmanCodePlusTimestamp)
    
    # if verification fails, huffman decoding will not be conducted.
       if verificationResult == 0:
        print("Invalid Authentication !!!")
        exit()
    # if verification succeeds, huffman decoding will be carried out and return recoveredDCT.
       elif verificationResult == 1:
         huffmanEncoderTablePath = "./myFolder/HuffmanFolder/codigos.txt"
         recoveredDCT, recoveredDCTTxtPath = huffmanDecoding(huffmanEncoderTablePath,huffmanCodeLessTimestamp)
         # Finally we conduct inverse DCT transform and get back 256x256 gray image
         finalImgPath = "./myFolder/ImgFolder/OutputImages/finalImage.jpg"
         finalImageGetBack = idtc.idtcMain(recoveredDCTTxtPath).save(finalImgPath)
        
        
      #   print(recoveredDCT)
        
          



main()
