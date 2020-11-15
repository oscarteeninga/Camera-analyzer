import React from "react";

const DeviceListItem = ({id, name, ip}) => {
    return (
        <div className="deviceListItem">
            <h4 className="camera">{name} ({ip})</h4>
        </div>
    );
};

export default DeviceListItem;