
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
        // Number of hours = number of milliseconds / 3,600,000
        this.hour = Math.floor(this.milliseconds_total / hour_factor)
        // How many milliseconds remain when the elapsed hours are subtracted
        let ms_left = this.milliseconds_total - (this.hour  * hour_factor)
        // Number of minutes when the hours are subtracted
        this.min = Math.floor(this.milliseconds_total / min_factor)-(this.hour * 60);
        // Number of milliseconds that remains after the hours and minutes are subtracted
        ms_left = ms_left - (this.min * min_factor)
        // Translate number of milliseconds left to seconds
        this.sec = Math.floor(ms_left / 1000);
        // Number of milliseconds left when seconds are subtracted
        this.ms = ms_left - (this.sec * 1000);
        // Translate the number of milliseconds to 100th of a second
        this.ms = Math.floor(this.ms / 100);
    }
    // get the string representation of the milliseconds
    toString() {
        let hours = null;
        let minutes = null;
        let seconds = null;
        let milliseconds = null;

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

        milliseconds = "" + this.ms;

        return hours + minutes + seconds + milliseconds;
    }
}

class Timer {

    /*
    @parameter : output_id
        The id of an HTML-Element that will be used for output of the Timer
    */
    constructor(output_id) {
        this.interval = 100;
        this.start_time = 0;
        // Variable for the intervals
        this.repeat = null;        
        this.stop_time = 0;           
        this.output = document.getElementById(output_id);
        // How much time elapsed between start_time and stop_time
        this.time_elapsed = 0;
    }

    start = () => {
        this.start_time = Date.now();
        this.repeat = setInterval(this.displayProgress, this.interval, this);
    }



    stop = () => {
        // Log the stop time
        this.stop_time = Date.now() - this.start_time;
        // Format the outgoing string
        let out = new TimerOutput(this.stop_time );
        // Copy the outgoing string to the output element
        this.output.value = out.toString();
        // Clear the interval
        clearInterval(this.repeat);
    }
    /*  Update the value of the HTML-Element by element_id,
        that was passed to the constructor        
    */
    displayProgress = () => {
        let ms_elapsed = Date.now() - this.start_time;
        // Format the outgoing string
        let out = new TimerOutput(ms_elapsed);
        // Copy the outgoing string to the output element
        this.output.value = out.toString();
    }
}