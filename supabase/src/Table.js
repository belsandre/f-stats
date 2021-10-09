import React from 'react';

const TableHeader = () => { 
    return (
        <thead>
            <tr>
                <th>Name</th>
                <th>City</th>
                <th>State</th>
            </tr>
        </thead>
    );
}

const TableBody = props => { 
    const rows = props.clinicData.map((row, index) => {
        return (
            <tr key={index}>
                <td>{row.name}</td>
                <td>{row.city}</td>
                <td>{row.state}</td>
            </tr>
        );
    });

    return <tbody>{rows}</tbody>;
}

const Table = (props) => {
    const { clinicData } = props;
        return (
            <table>
                <TableHeader />
                <TableBody clinicData={clinicData} />
            </table>
        );
}

export default Table;