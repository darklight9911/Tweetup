def prioritySort(patientList) -> list:
    
    if patientList == None:
        return []
    seriousPatients = []
    moderatePatients = []
    normalPatients = []
    
    for i in patientList:
        if i.severity.strip() == "Serious":
            seriousPatients.append(i)
        if i.severity.strip() == "Moderate":
            moderatePatients.append(i) 
        if i.severity.strip() == "Normal":
            normalPatients.append(i)
    
    seriousPatients.extend(moderatePatients)
    seriousPatients.extend(normalPatients)

    return seriousPatients
