
/*
    TimerOutput takes the amount of milliseconds in its constructor and converts it into 
    a String "mm:ss.ms"
*/
class TimerOutput {
    constructor(milliseconds) {
        this.milliseconds_total = milliseconds;
        this.ms = 0;
        this.sec = 0;
        this.min = 0;
        this.hour = 0;
        this.initializeFields();
    }

    initializeFields() {
        const min_factor = 60 * 1000;
        const hour_factor = min_factor * 60;

        this.hour = Math.floor(this.milliseconds_total / hour_factor)
        let ms_left = this.milliseconds_total - (this.hour  * hour_factor)
        this.min = Math.floor(this.milliseconds_total / min_factor)-(this.hour * 60);
        ms_left = ms_left - (this.min * min_factor)
        this.sec = Math.floor(ms_left / 1000);
        this.ms = ms_left - (this.sec * 1000);
        this.ms = Math.floor(this.ms / 100);
    }
    // get the string representation of the milliseconds
    toString() {
        let hours = null;
        let minutes = null;
        let seconds = null;
        let millis = null;

        if(this.hour < 10){
            hours = "0" + this.hour + ":";
        }else{
            hours = ""+ this.hour + ":";
        }

        if (this.min < 10) {
            minutes = "0" + this.min + ":";
        } else {
            minutes = "" + this.min + ":";
        }

        if (this.sec < 10) {
            seconds = "0" + this.sec + ":";
        } else {
            seconds = "" + this.sec + ":";
        }

        millis = "" + this.ms;

        return hours + minutes + seconds + millis;
    }
}

class Timer {

    /*
    @parameter : output_id
        The id of an HTML-Element that will be used for output of the progress

    @parameter : interval
        The interval (in milliseconds) in which the HTML-Element with the assigned output_id
        will be updated. 
    */
    constructor(output_id) {
        this.interval = 100;
        this.start_time = 0;
        this.repeat = null;
        this.counter = 0;
        this.stop_time = 0;        
        this.started = false;        
        this.output_id = output_id;
        this.time_elapsed = 0;
        this.run = null;
    }

    start = () => {
        if (this.started == false) {
            this.started = true;
            this.start_time = Date.now();
            this.repeat = setInterval(this.displayProgress, this.interval, this);
        }
    }



    stop = () => {
        this.started = false;

        this.stop_time = Date.now() - this.start_time;
        let out = new TimerOutput(this.stop_time );

        document.getElementById(this.output_id).value = out.toString();
        clearInterval(this.repeat);
    }

    reset = () => {
        this.start_time = Date.now();
        this.displayProgress(this);
    }

    /* 
        Update the value of the HTML-Element by element_id, that was passed to the constructor        
    */
    displayProgress = () => {
        let ms_elapsed = Date.now() - this.start_time;


        let out = new TimerOutput(ms_elapsed);
        document.getElementById(this.output_id).value = out.toString();
    }
}