slint::include_modules!();
use std::io::Write;

use serialport::prelude::*;

static mut PORT: Option<Box<dyn SerialPort>> = None;

fn main() -> Result<(), slint::PlatformError> {


    let ui = AppWindow::new()?;
    let ui_handle = ui.as_weak();
    let ui = ui_handle.unwrap();
  
    

    ui.on_send_values(move || {
    let _ui = ui_handle.unwrap();
    let data:&str = "test";
    let bytes_data: &[u8] = data.as_bytes();
    unsafe {
        if let Some(port) = &mut PORT {
            // Write data to the serial port
            port.write_all(bytes_data);
        } else {
            println!("Serial port is not open");
        }
    }
    });

    let ui_handle = ui.as_weak();
    ui.on_connect_to_port(move || {
        let ui = ui_handle.unwrap();

        let port_name = format!("{}", ui.get_portName());
        println!("{}", port_name);
        unsafe {
        if let Some(port) = &mut PORT {
            let port = match serialport::open_with_settings(&port_name, &SerialPortSettings {
                baud_rate: 9600,
                data_bits: DataBits::Eight,
                flow_control: FlowControl::None,
                parity: Parity::None,
                stop_bits: StopBits::One,
                timeout: std::time::Duration::from_secs(1),
            }){
                Ok(port) => port,
                Err(err) => {
                    eprintln!("Failed to open serial port: {}", err);
                    return; // Return early if failed to open the port
            }
        };
        };
    }
    });
    ui.run()
}
