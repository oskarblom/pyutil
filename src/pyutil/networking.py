class IpAddressFormatException(Exception): 
    pass

def valid_quad(quad):
    try:
        return len(bin(int(quad))) <= 10
    except TypeError:
        return False

class IpAddress(object):

    def __init__(self, q1, q2, q3, q4):
        if any(q for q in (q1, q2, q3, q4) if not valid_quad(q)):
            raise IpAddressFormatException
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    def to_int(self):
        return (self.q1 << 24) | (self.q2 << 16) | (self.q3 << 8) | self.q4

    @classmethod
    def parse(cls, ip_string):
        try:
            return cls(*map(int, (ip_string.split("."))))
        except AttributeError, TypeError:
            raise IpAddressFormatException

    @classmethod
    def from_int(cls, val):
        try:
            val = int(val)
            return cls(val >> 24,
                       val >> 16 & 0xFF,
                       val >> 8 & 0xFF,
                       val & 0xFF)
        except TypeError:
            raise IpAddressFormatException

    def __str__(self):
        return "%d.%d.%d.%d" % (self.q1, self.q2, self.q3, self.q4)

    def __repr__(self):
        return "IpAdress(%d, %d, %d, %d)" % (self.q1,
                                             self.q2,
                                             self.q3,
                                             self.q4)

class IpNetworkFormatException(Exception):
    pass

class IpNetwork(object):

    def __init__(self, desc, net_mask=24):
        try:
            ip, mask_bits = desc.split("/")
            mask_bits = int(mask_bits)

            ip = IpAddress.parse(ip)
            self.ip = ip

            shift = (32 - mask_bits)
            mask_int = sum(2 ** i for i in range(mask_bits)) << shift
            subnet_id_int = ip.to_int() & mask_int
            self.subnet_id = IpAddress.from_int(subnet_id_int)

        except ValueError:
            raise IpNetworkFormatException

    def __str__(self):
        return "IP: %s, Subnet ID: %s" % (self.ip, self.subnet_id)

if __name__ == "__main__":
    network2 = IpNetwork("82.25.1.69/28")
    print network2
    ip2 = IpAddress(12, 1, 127, 6)
    ip3 = IpAddress.parse("216.9.110.14")
    ip3int = ip3.to_int()
    print ip2
    print ip3int
    print IpAddress.from_int(ip3int).to_int() == ip3int
