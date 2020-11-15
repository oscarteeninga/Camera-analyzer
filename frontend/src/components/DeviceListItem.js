import React from "react";

const DeviceListItem = ({id, name}) => {
    return (
        <div className="deviceListItem">
            <h4 className="name">{name}</h4>
        </div>
    );
};

export default DeviceListItem;