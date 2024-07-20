const mongoose = require('mongoose');


let  userschema=new mongoose.Schema({
     username:{
          type:String,
          required:true,
          unique:true,
     },
     password:{
           type:Number,
           required:true,
           unique:true,
     }

})

module.exports=mongoose.model("user",userschema);
