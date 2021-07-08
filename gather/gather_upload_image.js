// From the gather repo in mini-conf...

const fs = require('fs')
const fsp = require('fs').promises;
const axios = require("axios");
// Some online image that can be used as placeholder in a poster when building a town. It's an icon for a zoom call.
const DEFAULT_IMAGE = "https://cdn.gather.town/v0/b/gather-town.appspot.com/o/assets%2Fb2c9fbf1-4fc1-4b59-9ef1-e3de6b69981f?alt=media&token=cb74684a-3c6e-4260-b51c-c917e078124d";

 // Uploads image file to gather town.
 // Usage: myUrl = exports.uploadImage("myFile.png")
 // If upload failed, will return the URL of some default image
async function uploadImage(mySpace, inFname) {
     let defaultImage = "";
     let data = {};
     try {
         data = await fsp.readFile(inFname, async function (err, data) {
             if (err) {
                 reject(err); // Fail if the file can't be read.
             }
         });
     } catch {
         console.log("Error reading " + inFname);
         return defaultImage;
     }
     let posterPath = await axios
         .post(
             "https://gather.town/api/uploadImage",
             {
                 bytes: data,
                 spaceId: mySpace,
             },
             { maxContentLength: Infinity, maxBodyLength: Infinity }
         )
         .then((res) => {
            //  console.log(inFname + " successfully uploaded");
            //  console.log(res.data);
             return res.data;
         })
         .catch((err) => {console.log("Error uploading " + inFname);
             return defaultImage});
     return posterPath;
 };

 let myArgs = process.argv.slice(2);
 let mySpace = myArgs[0];
 let file = myArgs[1];
 uploadImage(mySpace, file).then((res) => console.log(res.trim()));
