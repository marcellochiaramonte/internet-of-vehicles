package de.rub.enesys.ovms3lite.repository;

import de.rub.enesys.ovms3lite.model.Location;
import de.rub.enesys.ovms3lite.model.Vehicle;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface LocationRepository extends CrudRepository<Location,Long> {

}
