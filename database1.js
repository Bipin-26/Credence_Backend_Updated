const express = require("express");
const mongoose = require("mongoose");
const winston = require("winston")

const app = express()

const bodyParser=require("body-parser")

app.use(bodyParser.urlencoded({extended: false}));

const movielist= require('./data_modules/data.json')
const server = require('./data_modules/server.json')
const db = require("./data_modules/db.json")

var logger = winston.createLogger({
    level:'info',
    format:winston.format.json(),
    transports: [
      new (winston.transports.Console)(),
      new (winston.transports.File)({ filename: 'log_file.log' })
    ]
  });

if (process.env.NODE_ENV !== 'production') {
logger.add(new winston.transports.Console({
    format: winston.format.simple(),
}));
}

try{
    mongoose.connect(`${db['database']}://${db['hostname']}:${db['port']}/${db['dbname']}`);
    logger.info("Database Connection Successful")
} catch (err){
    logger.info("Connection Failed")
    logger.error(err)
}

var movieSchema = new mongoose.Schema({
    name:String,
    img:String,
    summary:String
});

var Movie = mongoose.model("Movie",movieSchema,"moviestore"); 
 
app.get('/display',(req,res)=>{
    try{
        Movie.find({},(err,docs)=>{
            if(err){
                res.send(err)
            }
            else{
                if(docs.length == 0){
                    res.json({message:"No Movies found"})
                    logger.info("No Movies Found")
                }
                else{
                    res.json({message:"Value found",values:docs})
                }  
                
            }
        })
    } catch(err){
        res.json({message:"Something went wrong. Cant add value"})
        logger.error(err)
    }
    
})


app.post('/insert',(req,res)=>{
    try{
        Movie.collection.insertMany(movielist,(err,docs)=>{
            if(err){
                logger.error(err)
                res.json({message:"Something went wrong. Cant add value"})
            }
            else{
                res.json({message:"Values added successfully",TotalCount:`${docs['insertedCount']}`})
                logger.info("Values added")
            }
        })
    }
    catch{
        logger.error(err)
    }
})

app.post('/insert_one',(req,res)=>{
    try{
        response={
            "name":req.body.name,
            "img":req.body.img,
            "summary":req.body.summary
        }
        Movie.collection.insertOne(response,(err,docs)=>{
            if(err){
                res.json({message:"Something went wrong. Cant add value"})
                logger.error(err)
            }
            else{
                res.json({message:"Value added successfully.....!!!",id:docs['insertedId']})
                logger.info("Value added")
            }
        })
    }
    catch{
        logger.error(err)
    }
})

app.listen(server['port'],()=>{
    console.log(`Server running at http://${server['hostname']}:${server['port']}`);
}).on('error',(err)=>{
    if (err.code === 'EADDRINUSE'){
        logger.error(err)
    }
});



