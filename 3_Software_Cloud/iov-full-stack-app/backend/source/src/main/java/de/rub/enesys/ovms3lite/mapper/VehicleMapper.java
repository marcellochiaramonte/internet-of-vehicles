package de.rub.enesys.ovms3lite.mapper;

import de.rub.enesys.ovms3lite.dto.output.VehicleForListOutput;
import de.rub.enesys.ovms3lite.model.Vehicle;
import org.mapstruct.Mapper;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

import java.util.List;

@Mapper(unmappedSourcePolicy = ReportingPolicy.IGNORE,
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.SET_TO_DEFAULT)
public interface VehicleMapper {

    VehicleMapper INSTANCE = Mappers.getMapper(VehicleMapper.class);

    VehicleForListOutput vehicleOutputForVehicleList(Vehicle vehicle);

    List<VehicleForListOutput> vehicleOutputListForVehicleList(List<Vehicle> vehicleList);
}
