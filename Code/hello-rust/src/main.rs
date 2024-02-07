extern crate serialport;
use serialport::prelude::*;
fn main() {
    println!("Hello, world!");
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }

}
