slint::include_modules!();
use serialport::prelude::*;


fn main() -> Result<(), slint::PlatformError> {


    let ui = AppWindow::new()?;
    let ui_handle = ui.as_weak();
    let ui = ui_handle.unwrap();
    
    ui.on_send_values(move || {
        let ui = ui_handle.unwrap();
        println!("{}", ui.get_xALegxH());
    });

    let ui_handle = ui.as_weak();
    ui.on_connect_to_port(move || {
        let ui = ui_handle.unwrap();
        println!("{}", ui.get_portName());
        let temp_Port = format!("{}{}", "{}", ui.get_portName());
        //format!("{}{}", "{}", ui.get_portName());
        let port_name = format!("{}", temp_Port); 
        let port = serialport::open_with_settings(&port_name, &SerialPortSettings {
            baud_rate: 9600,
            data_bits: DataBits::Eight,
            flow_control: FlowControl::None,
            parity: Parity::None,
            stop_bits: StopBits::One,
            timeout: std::time::Duration::from_secs(1),
        }).expect("Failed to open serial port");
    });
    ui.run()
}
